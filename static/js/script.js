window.addEventListener("load", () => {
    const laoder = document.querySelector(".loader");

    laoder.classList.add("loader-hidden");

    laoder.addEventListener("transitioned", () => {
        document.body.removeChild("laoder");
    })
})