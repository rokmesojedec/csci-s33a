(() => {

    // draws images in canvas, using the Square class
    // divides the canvas in to grid, with each grid unit corresponding to size defined in Square
    // the algorithm then fills the canvas grid with instances of Square class - each one defining 
    // shape, colors of each grid unit - until whole canvas is filled
    let drawImage = function(animate, colors, size, width, height, circleChance, colorChance, fourPartChance){
        const canvasWidth = width * size;
        const canvasHeight = height * size;

        const canvas = document.querySelector("canvas");
        const ctx = canvas.getContext("2d");

        ctx.canvas.width = canvasWidth;
        ctx.canvas.height = canvasHeight;


        // configures the Square constructor's static variables
        Square.widthEnd = canvasWidth;
        Square.heightEnd = canvasHeight;
        Square.colors = colors;
        Square.size = size;
        Square.circleChance = circleChance;
        Square.inheritColorChance = colorChance;
        Square.takenSpace.length = 0;
        Square.fourPartElementChance = fourPartChance;

        // prepares canvas context, prefills it with gray color
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.rect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "gray";
        ctx.fill();

        let numberXSquares = Math.ceil(canvas.width / Square.size);
        let numberYSquares = Math.ceil(canvas.height / Square.size);

        // randomly picks starting point
        let x = Math.floor(Math.random() * numberXSquares) * Square.size;
        let y = Math.floor(Math.random() * numberYSquares) * Square.size;

        let sq, preceedingSquare = null;
        let nextLocation = new Point(x, y);

        // disables saves button - user should not save image while it's being rendered
        let saveButton = document.querySelector("button.save");
        if (saveButton != null)
            saveButton.disabled = true;

        // draws one square, if an empty grid slot is available, then draws next. stops when no slots are left
        let draw = function () {
            sq = new Square({ start: nextLocation, ctx: ctx, previousSquare: preceedingSquare });
            preceedingSquare = sq;
            sq.draw();
            nextLocation = sq.getNextLocation();
            if (nextLocation != null) {if(animate) window.requestAnimationFrame(draw); else draw(); }
            else if (sq.previousSquare != null) {
                let previousSquare = sq.previousSquare;
                nextLocation = previousSquare.getNextLocation();
                while (previousSquare != null && nextLocation == null) {
                    previousSquare = previousSquare.previousSquare;
                    if (previousSquare != null)
                        nextLocation = previousSquare.getNextLocation();
                }
                if (nextLocation != null) {
                    preceedingSquare = previousSquare;
                    if(animate) window.requestAnimationFrame(draw); else draw();
                }else {
                    if(saveButton != null)
                    saveButton.disabled = false;
                }
            }
        }
        if(animate) window.requestAnimationFrame(draw); else draw();
    }   

    document.addEventListener("DOMContentLoaded", function () {
        const id = document.querySelector("#config_id").value;
        const tokenContainer = document.querySelector("input[name='csrfmiddlewaretoken']");
        // Get the CSRF Token from hidden field
        const csrfToken = (tokenContainer !== null) ? tokenContainer.value : null;

        // gets config from server
        ajax("GET", api.config.json.GET(id)).then(data=>{
            document.querySelector(".config-data code").innerHTML = JSON.stringify(data, null, 1);
            let { colors, circleChance, colorChance, fourPartChance, size, width, height, animate } = data;
            let saveButton = document.querySelector("button.save");

            // processes config data, makes sure it's in right data type
            colors = JSON.parse(colors);
            size = parseInt(size);
            width = parseInt(width);
            height = parseInt(height);
            circleChance = parseInt(circleChance) * 0.01;
            colorChance = parseInt(colorChance) * 0.01;
            fourPartChance = parseInt(fourPartChance) * 0.01;

            // draws image
            drawImage(animate, colors, size, width, height, circleChance, colorChance, fourPartChance);
           
            // adds onclick for regenrating the image
            let regenerateButton = document.querySelector("button.regen");
                regenerateButton.onclick = function(event){
                    drawImage(animate, colors, size, width, height, circleChance, colorChance, fourPartChance);
                };

            // save image event
            // image should not be savaed during render animation
            if(saveButton != null)
            saveButton.onclick = function(event){
                event.preventDefault();
                //saves image to server, redirects to showcase page once done
                ajax("PUT", api.config.upload.POST(id),{ 
                        body: JSON.stringify({ 'image':  document.querySelector("canvas").toDataURL() }),
                        headers: { "X-CSRFToken": csrfToken }
                    }, false)
                    .then(()=>{
                        window.location = "/";
                    }).catch(err=>console.error(err));
            };
        })
    })
})()