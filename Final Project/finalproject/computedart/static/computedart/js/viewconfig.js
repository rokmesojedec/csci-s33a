(() => {
    document.addEventListener("DOMContentLoaded", function () {
        id = document.querySelector("#config_id").value;

        ajax("GET", api.config.json.GET(id)).then(data=>{
            console.log(JSON.parse(data.colors));

            const canvas = document.querySelector("canvas");
            const ctx = canvas.getContext("2d");
    
            ctx.canvas.width = window.innerWidth;
            ctx.canvas.height = window.innerHeight;
    
            Square.widthEnd = window.innerWidth;
            Square.heightEnd = window.innerHeight;
            Square.colors = JSON.parse(data.colors);
            Square.size = parseInt(data.grid);
    
            ctx.lineWidth = 1;
    
            let evenWidth = canvas.width;
            let evenHeight = canvas.height;
    
            ctx.beginPath();
            ctx.rect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "gray";
            ctx.fill();
    
    
            for (let i = 2; i < evenHeight && i < evenWidth; i++) {
                if (evenWidth % i == 0 && evenHeight % i == 0)
                    console.log(i)
            }
            let numberXSquares = Math.ceil(canvas.width / Square.size);
            let numberYSquares = Math.ceil(canvas.height / Square.size);
    
            let x = Math.floor(Math.random() * numberXSquares) * Square.size;
            let y = Math.floor(Math.random() * numberYSquares) * Square.size;
    
            var sq, preceedingSquare = null;
            var nextLocation = new Point(x, y);
    
            let drawCircle = function () {
                sq = new Square({ start: nextLocation, ctx: ctx, previousSquare: preceedingSquare });
                preceedingSquare = sq;
                sq.draw();
                nextLocation = sq.getNextLocation();
                if (nextLocation != null) window.requestAnimationFrame(drawCircle);
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
                        window.requestAnimationFrame(drawCircle);
                    }
                }
            }
    
            window.requestAnimationFrame(drawCircle);
        })

       
    })
})()