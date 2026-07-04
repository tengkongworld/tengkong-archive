console.log("theme.js loaded");

function initializeTheme() {

    const savedTheme =

        localStorage.getItem(
            "theme"
        ) || "default";

    setTheme(
        savedTheme
    );

}

function setTheme(theme) {

    document.body.classList.remove(
        "eye",
        "dark",
        "classic"
    );

    if (
        theme !== "default"
    ) {

        document.body.classList.add(
            theme
        );

    }

    localStorage.setItem(
        "theme",
        theme
    );

    document
        .querySelectorAll(".theme-button")
        .forEach(button => {

            button.classList.toggle(

                "active",

                button.dataset.theme === theme

            );

        });

}

function getCurrentTheme() {

    return (

        localStorage.getItem(
            "theme"
        ) || "default"

    );

}