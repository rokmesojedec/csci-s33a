(() => {
    document.addEventListener("DOMContentLoaded", function () {
        const addColorButton = document.querySelector("button[value='add_color']");
        document.querySelectorAll(".color-config").forEach(input=>{
            console.log(input)
            input.value="#"+randomColor()})
        addColorButton.onclick = function (event) {
            event.preventDefault();
            let nextId = document.querySelectorAll(".color-config").length + 1;
            let form = document.querySelector("form");

            let removeButton = $("button", { innerHTML : "remove"});
                removeButton.addEventListener("click", function(){
                this.parentElement.parentElement.parentElement.remove();
            })
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
            console.log(randomColor())

            form.insertBefore(element, addColorButton);
        };
    });
})();

/* <div class="form-row colors">
<div class="form-group col-md-12 mb-2">
    <label for="color-2" class=" requiredField">
        Color 2<span class="asteriskField">*</span>
    </label>
    <div>
        <input type="color" class="color-config" name="color-2" />
    </div>
</div>
</div> */