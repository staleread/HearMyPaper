package hmp.authz

import data.workload_registry
import data.confidentiality_lattice

default allow = false

# --- JWT Decoding ---

# Decode the user token (passed in input.user_token)
user_payload := payload {
    [_, payload, _] := io.jwt.decode(input.user_token)
}

# --- Helper Rules ---

# Get workload properties for a given SPIFFE ID
workload_info(spiffe_id) = info {
    info := workload_registry[spiffe_id]
}

# Find the numeric index of a security level in the lattice
level_index(level) = i {
    confidentiality_lattice.levels[i] == level
}

# --- Authorization Logic (Stacked Authorization) ---

# A subject (user or workload) is authorized for an action on a resource level
authorize_subject(subject_claims, action, resource_level) {
    # 1. Confidentiality: No Read Up
    action == "read"
    level_index(subject_claims.confidentiality_level) >= level_index(resource_level)
}

authorize_subject(subject_claims, action, resource_level) {
    # 2. Confidentiality: No Write Down
    action == "write"
    level_index(subject_claims.confidentiality_level) <= level_index(resource_level)
    
    # 3. Integrity: Must have the integrity level for writing
    some i
    subject_claims.integrity_levels[i] == resource_level
}

# --- Main Authorization Rule ---

# Input expected:
# {
#   "workload_id": "spiffe://hmp.internal/...",
#   "user_token": "<JWT_STRING>",
#   "action": "read" | "write",
#   "resource_level": "RESTRICTED"
# }

allow {
    # Verify Workload
    workload_claims := workload_info(input.workload_id)
    authorize_subject(workload_claims, input.action, input.resource_level)

    # Verify User (from JWT)
    # The JWT payload is expected to have 'confidentiality_level' and 'integrity_levels'
    authorize_subject(user_payload, input.action, input.resource_level)
}
