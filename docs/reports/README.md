# Lab reports

We are using [typst](https://typst.app/) for writing reports, [d2](https://d2lang.com/) for the diagrams.

To compile a `.typ` report file, we need to pass the `--root` argument, so we can
import the diagrams from outside of the `reports` folder (here).

Example usage
```bash
typst w 07_security-policy.typ pdf/07_security-policy.pdf --root ..
```

