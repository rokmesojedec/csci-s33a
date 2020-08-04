(() => {
    document.addEventListener("DOMContentLoaded", function () {

        const addColorButton = document.querySelector("button[value='add_color']");

        // Populate color pickers with random HEX values
        document.querySelectorAll(".color-config").forEach(input => {
            input.value = "#" + randomColor()
        })

        // Add color picker input on "Add Color" button click
        addColorButton.onclick = function (event) {
            event.preventDefault();
            let nextId = document.querySelectorAll(".color-config").length + 1;
            let form = document.querySelector("form");

            // For added Color inputs, add remove button also
            let removeButton = $("button", { innerHTML: "Remove", attributes: { class: "ml-3 btn btn-danger btn-sm" } });
            // Remove button, removes color picker, changes subsequent color picker names - adjusts indexing
            removeButton.addEventListener("click", function () {
                this.parentElement.parentElement.parentElement.remove();
                let index = 1;
                document.querySelectorAll(".colors").forEach(element => {
                    let label = element.querySelector("label")
                    label.setAttribute("for", "color-" + index)
                    label.innerHTML = "Color " + index;
                    let input = element.querySelector("input");
                    input.setAttribute("name", "color-" + index);
                    index++;
                })
            })

            // Creates color picker element and adds it to DOM
            let element = $("div", {
                attributes: { class: "form-row colors" },
                innerHTML: $("div", {
                    attributes: { class: "form-group col-md-12 mb-2" },
                    innerHTML: [
                        $("label", { innerHTML: ["Color " + nextId, $("span", { innerHTML: "*", attributes: { class: "asteriskField" } })] }),
                        $("div", {
                            innerHTML: [
                                $("input", {
                                    attributes: {
                                        type: "color",
                                        class: "color-config",
                                        name: "color-" + nextId,
                                        value: `#${randomColor()}`
                                    }
                                }),
                                removeButton
                            ]
                        })
                    ]
                })
            });
            form.insertBefore(element, addColorButton);
        };
    });
})();