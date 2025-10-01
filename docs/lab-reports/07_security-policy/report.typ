#set page(
  paper: "a4",
  margin: (
    top: 20mm,
    bottom: 20mm,
    left: 25mm,
    right: 15mm,
  ),
)

#set par(
  first-line-indent: (
    amount: 1.25cm,
    all: true,
  ),
  justify: true,
  leading: 1.5em,
)

#let fontSize = 14pt;

#set text(
  font: "Times New Roman",
  size: fontSize,
)

#set figure(
  supplement: [Рисунок],
  numbering: _ => {
    let headingCnt = str(counter(heading).get().at(0));
    let figureCnt = str(counter(figure).get().at(0));

    headingCnt + "." + figureCnt
  }
)

#set figure.caption(
  separator: [ -- ],
)

#set heading(numbering: (..nums) => {
   let numbers = nums.pos()

   if numbers.len() == 2 {
      numbering("1.1.", ..numbers)
   }
})

#show heading.where(level: 1): it => {
  // reset figure timer inside top-level heading body
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

#show heading.where(level: 2): it => {
  set text(size: fontSize);

  block(
    above: 3.5em,
    below: 2.5em,
    it,
  )
}

#show outline: it => {
  show heading: set align(center)
  it
}

#align(center)[
  #set par(leading: 1em)
  *Міністерство освіти і науки України* \
  *Чернівецький національний університет імені Юрія Федьковича* \
  \
  Інститут фізико-технічних та комп’ютерних наук \
  Кафедра програмного забезпечення комп’ютерних систем
]

#align(center + horizon)[
  #upper[ *Звіт* ] \

  #set par(leading: 1em)
  про виконання лабораторної роботи №7 \
  з курсу "Безпека програм та даних" \
  \
  Тема: Підсистема керування доступом \
  \
  Виконали: Неголюк О.О., Ратушняк М.А. \
  Перевірив: Остапов С.Е. \
]

#align(center + bottom)[
  Чернівці -- 2025
]
#pagebreak()

#set par(
  leading: 1.5em,
)

#outline(title: upper[Зміст])
#pagebreak()

= ЗРАЗОК ЗАГОЛОВКУ

#lorem(40)

#lorem(40)

#figure(
  image("read-access.svg"),
  caption: [Діаграма політики доступу для "читання" об'єктів]
)

#figure(
  image("write-access.svg"),
  caption: [Діаграма політики доступу для "створення" об'єктів]
)

#figure(
  image("data-flow.svg"),
  caption: [Data Flow діаграма системи HearMyPaper]
)

#figure(
  image("use-case.svg"),
  caption: [Діаграма прецедентів системи HearMyPaper]
)

#pagebreak()

= ВІДПОВІДІ НА КОНТРОЛЬНІ ЗАПИТАННЯ

*1. Проаналізуйте недоліки довірчого управління доступом.*

#lorem(15)

*2. Оцініть позитивні та негативні сторони реалізованої політики безпеки.*

#lorem(15)

*3. Опишіть на рівні структур даних, як у Вашій роботі реалізовано матрицю доступу.*

#lorem(15)

*4. Охарактерізуйте рівень контролю доступу в реалізованій системі згідно НД ТЗІ 2.5-004-99. Що можна зробити, щоб його підвищити?*

#lorem(15)

*5. Проаналізуйте взаємодію підсистеми управління доступом автентифікації в розробленій системі*

#lorem(15)

#pagebreak()

= ВИСНОВКИ

#lorem(40)
