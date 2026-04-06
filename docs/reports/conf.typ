#let lab_report(
  num: 1,
  subject: "Example subject",
  title: "Example title",
  authors: (),
  reviewer: "Name Surname",
  year: 2025,
  doc
) = {
  set page(
    paper: "a4",
    margin: (
      top: 20mm,
      bottom: 20mm,
      left: 25mm,
      right: 15mm,
    ),
  )

  set par(
    first-line-indent: (
      amount: 1.25cm,
      all: true,
    ),
    justify: true,
    leading: 1.5em,
  )

  let fontSize = 14pt;

  set text(
    font: "Times New Roman",
    size: fontSize,
  )

  set figure(
    supplement: [Рисунок],
    numbering: _ => {
      let headingCnt = str(counter(heading).get().at(0));
      let figureCnt = str(counter(figure).get().at(0));
      headingCnt + "." + figureCnt
    }
  )

  set figure.caption(separator: [ -- ])

  set heading(numbering: (..nums) => {
     let numbers = nums.pos()
     if numbers.len() == 2 {
        numbering("1.1.", ..numbers)
     }
  })

  show heading.where(level: 1): it => {
    counter(figure).update(0)
    align(center)[
      #set text(size: fontSize)
      #block(
        above: 3.5em,
        below: 2.5em,
        it,
      )
    ]
  }

  show heading.where(level: 2): it => {
    set text(size: fontSize);
    block(above: 3.5em, below: 2.5em, it)
  }

  show outline: it => {
    show heading: set align(center)
    it
  }

  show raw.where(block: true): it => {
    set par(first-line-indent: 0pt)
    set text(font: "Courier New", size: 10pt)
    it
  }

  let authors_text = if authors.len() > 1 {
    "Виконали: " + authors.join(", ")
  } else {
    "Виконав: " + authors.at(0)
  }

  align(center)[
    #set par(leading: 1em)
    *Міністерство освіти і науки України* \
    *Чернівецький національний університет імені Юрія Федьковича* \
    \
    Інститут фізико-технічних та комп’ютерних наук \
    Кафедра програмного забезпечення комп’ютерних систем
  ]

  align(center + horizon)[
    #upper[*Звіт*] \

    #set par(leading: 1em)
    про виконання лабораторної роботи №#num \
    з курсу "#subject" \
    \
    Тема: #title \
    \
    #authors_text \
    Перевірив: #reviewer \
  ]

  align(center + bottom)[
    Чернівці -- #year
  ]

  pagebreak()

  outline(title: upper[Зміст])
  pagebreak()

  doc
}
