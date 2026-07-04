
const DEFAULT_FONT_SIZE = 18;

const MIN_FONT_SIZE = 14;

const MAX_FONT_SIZE = 24;

function applyFontSize(size) {

    const content =

        document.querySelector(".article-content")

        ||

        document.querySelector(".article-list");

    if (!content) {

        return;

    }

    content.style.fontSize = size + "px";

    localStorage.setItem(

        "fontSize",

        size

    );

    const value =

        document.getElementById("font-size");

    if (value) {

        value.textContent = size;

    }

}

function initializeFontSize() {

    let size = parseInt(

        localStorage.getItem("fontSize")

    );

    if (isNaN(size)) {

        size = DEFAULT_FONT_SIZE;

    }

    applyFontSize(size);

}
if (window.currentArticle) {

    /* 最近阅读 */

    let history = JSON.parse(

        localStorage.getItem(
            "readingHistory"
        ) || "[]"

    );

    history = history.filter(

        item => item.url !== window.currentArticle.url

    );

    history.unshift(

        window.currentArticle

    );

    history = history.slice(

        0,

        10

    );

    localStorage.setItem(

        "readingHistory",

        JSON.stringify(history)

    );



    /* 累计阅读 */

    let archive = JSON.parse(

        localStorage.getItem(
            "readingArchive"
        ) || "[]"

    );

    if (

        !archive.includes(
            window.currentArticle.url
        )

    ) {

        archive.push(

            window.currentArticle.url

        );

        localStorage.setItem(

            "readingArchive",

            JSON.stringify(
                archive
            )

        );

    }

}

/* 初始化主题 */

initializeTheme();

initializeFontSize();

/* Theme 按钮 */

document

    .querySelectorAll(".theme-button")

    .forEach(button => {

        button.addEventListener(

            "click",

            () => {

                setTheme(

                    button.dataset.theme

                );

            }

        );

    });

const smaller =

    document.getElementById(

        "font-smaller"

    );

const larger =

    document.getElementById(

        "font-larger"

    );

if (smaller) {

    smaller.addEventListener(

        "click",

        () => {

            let size = parseInt(

                localStorage.getItem(

                    "fontSize"

                )

            ) || DEFAULT_FONT_SIZE;

            if (size > MIN_FONT_SIZE) {

                applyFontSize(

                    size - 1

                );

            }

        }

    );

}

if (larger) {

    larger.addEventListener(

        "click",

        () => {

            let size = parseInt(

                localStorage.getItem(

                    "fontSize"

                )

            ) || DEFAULT_FONT_SIZE;

            if (size < MAX_FONT_SIZE) {

                applyFontSize(

                    size + 1

                );

            }

        }

    );

}