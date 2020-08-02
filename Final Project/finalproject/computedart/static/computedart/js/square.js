class Point {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}


class Square {
    constructor({ start = new Point(), ctx = null, previousSquare = null }) {
        this.start = start;
        this.end = new Point(
            start.x + this.constructor.size,
            start.y + this.constructor.size);
        this.ctx = ctx;
        this.previousSquare = previousSquare;

        Square.takenSpace.push(this.start);

        this.availablePaths = [];

        //left
        if ((this.start.x - Square.size) >= 0 && !this.isLocationTaken(this.start.x - Square.size, this.start.y)) this.availablePaths.push(new Point(this.start.x - Square.size, this.start.y));
        //right
        if ((this.start.x + Square.size) <= Square.widthEnd && !this.isLocationTaken(this.start.x + Square.size, this.start.y)) this.availablePaths.push(new Point(this.start.x + Square.size, this.start.y));
        //up
        if ((this.start.y - Square.size) >= 0 && !this.isLocationTaken(this.start.x, this.start.y - Square.size)) this.availablePaths.push(new Point(this.start.x, this.start.y - Square.size));
        //down
        if ((this.start.y + Square.size) <= Square.heightEnd && !this.isLocationTaken(this.start.x, this.start.y + Square.size)) this.availablePaths.push(new Point(this.start.x, this.start.y + Square.size));
    }

    isLocationTaken(x, y) {
        for (let i = 0; i < Square.takenSpace.length; i++) {
            let point = Square.takenSpace[i];
            if (point.x == x && point.y == y) return true;
        }
        return false;
    }

    getNextLocation() {
        if (this.availablePaths.length == 0) return null;
        let pickIndex = Math.floor(Math.random() * this.availablePaths.length);
        let location = this.availablePaths.splice(pickIndex, 1)[0];
        if (this.isLocationTaken(location.x, location.y)) return this.getNextLocation();
        return location;
    }


  
    randomColor() {
        console.log(Square.colors[Math.floor(Math.random() * Square.colors.length)])
        return Square.colors[Math.floor(Math.random() * Square.colors.length)];
    }
    draw() {
        if (Math.random() < 0.15) {
            this.drawShape({ shape: "square", color: this.randomColor() });
            this.drawShape({ shape: "circle", color: this.randomColor() });
        }
        else {
            let color1, color2;
                color1 = this.randomColor();
                color2 = this.randomColor();
           
            this.drawShape({ shape: "top", color: this.randomColor() });
            this.drawShape({ shape: "left", color: this.randomColor() });
            this.drawShape({ shape: "bottom", color: this.randomColor() });
            this.drawShape({ shape: "right", color: this.randomColor() });
        }
        // this.drawQuadrant({ position: "left", color: Square.colors[Math.floor(Math.random() * Square.colors.length)] });
        // this.drawQuadrant({ position: "right", color: Square.colors[Math.floor(Math.random() * Square.colors.length)] });
    }

    drawShape({
        shape = "top",
        color = "black"
    } = {}) {
        let firstPoint = null, secondPoint = null, thirdPoint = null;
        let halfSize = Math.ceil(this.constructor.size / 2);


        if (shape == "circle") {
            let ctx = this.ctx;
            ctx.beginPath();
            ctx.fillStyle = color;
            ctx.strokeStyle = color;
            ctx.lineWidth = 1;
            ctx.arc(this.start.x + halfSize, this.start.y + halfSize, halfSize-1, 0, 2 * Math.PI);
            ctx.fill();
        }
        else if (shape == "square") {
            let ctx = this.ctx;
            ctx.beginPath();
            ctx.fillStyle = color;
            ctx.strokeStyle = color;
            ctx.lineWidth = 1;
            ctx.moveTo(this.start.x, this.start.y);
            ctx.lineTo(this.end.x, this.start.y);
            ctx.lineTo(this.end.x, this.end.y);
            ctx.lineTo(this.start.x, this.end.y);
            ctx.fill();
        } else {
            switch (shape.toLowerCase()) {
                case "top":
                    firstPoint = new Point(this.start.x, this.start.y);
                    secondPoint = new Point(this.end.x, this.start.y);
                    thirdPoint = new Point(this.start.x + halfSize, this.start.y + halfSize)
                    break;
                case "bottom":
                    firstPoint = new Point(this.start.x, this.end.y);
                    secondPoint = new Point(this.end.x, this.end.y);
                    thirdPoint = new Point(this.start.x + halfSize, this.start.y + halfSize)
                    break;
                case "left":
                    firstPoint = new Point(this.start.x, this.start.y);
                    secondPoint = new Point(this.start.x, this.end.y);
                    thirdPoint = new Point(this.start.x + halfSize, this.start.y + halfSize)
                    break;

                case "right":
                    firstPoint = new Point(this.end.x, this.start.y);
                    secondPoint = new Point(this.end.x, this.end.y);
                    thirdPoint = new Point(this.start.x + halfSize, this.start.y + halfSize)
                    break;
                case "topright": {
                    firstPoint = new Point(this.start.x, this.start.y);
                    secondPoint = new Point(this.end.x, this.start.y);
                    thirdPoint = new Point(this.end.x, this.end.y);
                    break;
                }
                case "bottomleft": {
                    firstPoint = new Point(this.start.x, this.start.y);
                    secondPoint = new Point(this.start.x, this.end.y);
                    thirdPoint = new Point(this.end.x, this.end.y)
                    break;
                }
            }
            if (this.ctx != null) {
                let ctx = this.ctx;
                ctx.beginPath();
                ctx.fillStyle = color;
                ctx.strokeStyle = color;
                ctx.lineWidth = 1;
                ctx.moveTo(firstPoint.x, firstPoint.y);
                ctx.lineTo(secondPoint.x, secondPoint.y);
                ctx.lineTo(thirdPoint.x, thirdPoint.y);
                ctx.fill();
            }
        }
    }
}
Square.size = 80;
Square.widthEnd = null;
Square.heightEnd = null;
Square.colors = [];
Square.takenSpace = [];