class Point {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

// Square class
// defines grid square, which populates a grid on canvas
// each square can have sub-elements of different colors
// backtracking is used to populate the canvas 
class Square {
    constructor({ start = new Point(), ctx = null, previousSquare = null, twoPieceElement = false }) {
        this.start = start;
        this.twoPieceElement = twoPieceElement;
        this.end = new Point(
            start.x + this.constructor.size,
            start.y + this.constructor.size);
        this.ctx = ctx;
        this.previousSquare = previousSquare;
        this.availablePaths = [];
        Square.takenSpace.push(this.start);
        //left
        if ((this.start.x - Square.size) >= 0 && !this.isLocationTaken(this.start.x - Square.size, this.start.y)) this.availablePaths.push(new Point(this.start.x - Square.size, this.start.y));
        //right
        if ((this.start.x + Square.size) <= Square.widthEnd && !this.isLocationTaken(this.start.x + Square.size, this.start.y)) this.availablePaths.push(new Point(this.start.x + Square.size, this.start.y));
        //up
        if ((this.start.y - Square.size) >= 0 && !this.isLocationTaken(this.start.x, this.start.y - Square.size)) this.availablePaths.push(new Point(this.start.x, this.start.y - Square.size));
        //down
        if ((this.start.y + Square.size) <= Square.heightEnd && !this.isLocationTaken(this.start.x, this.start.y + Square.size)) this.availablePaths.push(new Point(this.start.x, this.start.y + Square.size));
    }

    // tells where the passed square is located relative to current square
    getAdjecentSquareOrientation(square) {
        
        if (this.start.x - Square.size == square.start.x && square.start.y == this.start.y) return "left";
        if (this.start.x == square.start.x && square.start.y - Square.size == this.start.y) return "top";
        if (this.start.x + Square.size == square.start.x && square.start.y == this.start.y) return "right";
        if (this.start.x == square.start.x && square.start.y + Square.size == this.start.y) return "bottom";
        return null;
    }

    // gets color from previous adjecent square
    getPreviousSquareColor() {
        if (this.previousSquare == null) return null;
        if (this.previousSquare.square != null) return this.previousSquare.square.color;
        else switch (this.getAdjecentSquareOrientation(this.previousSquare)) {
            case "top":
                return this.previousSquare.bottom.color;
            case "bottom":
                return this.previousSquare.top.color;
            case "right":
                return this.previousSquare.left.color;
            case "left":
                return this.previousSquare.right.color;
        }
    }

    // checks if location is already populated
    isLocationTaken(x, y) {
        for (let i = 0; i < Square.takenSpace.length; i++) {
            let point = Square.takenSpace[i];
            if (point.x == x && point.y == y) return true;
        }
        return false;
    }

    // determins location of next element
    getNextLocation() {
        if (this.availablePaths.length == 0) return null;
        let pickIndex = Math.floor(Math.random() * this.availablePaths.length);
        let location = this.availablePaths.splice(pickIndex, 1)[0];
        if (this.isLocationTaken(location.x, location.y)) return this.getNextLocation();
        return location;
    }

    // gets random color or color from previous square
    getColor() {
        if (this.previousSquare == null || Math.random() < (1 - Square.inheritColorChance)) return this.randomColor();
        else return this.getPreviousSquareColor()
    }

    // picks random color from pallet
    randomColor() {
        return Square.colors[Math.floor(Math.random() * Square.colors.length)];
    }

    // draws element - either square with circle inside or square formed out of four triangles
    // each sub-element can have its own color
    draw() {
        if (Math.random() <= Square.circleChance) {
            let color1 = this.getColor(), color2 = this.getColor();
            // make sure the two colors are not the same
            while (color1 == color2) {
                color2 = this.randomColor();
            }
            this.drawShape({ shape: "square", color: color1 });
            this.drawShape({ shape: "circle", color: color2 });
        } else if (false){
            this.drawShape({ shape: "top", color: this.getColor() });
            this.drawShape({ shape: "left", color: this.getColor() });
            this.drawShape({ shape: "bottom", color: this.getColor() });
            this.drawShape({ shape: "right", color: this.getColor() });
        }
        else {
            this.drawShape({ shape: "topleft",   color: this.getColor() });
            this.drawShape({ shape: "bottomright", color: this.getColor() });
        }
    }

    // draws sub-element inside grid unit 
    drawShape({
        shape = "top",
        color = "black"
    } = {}) {

        if (shape == "bottomright"){
            this["bottom"] = { color: color };
            this["right"] = { color: color };
        } else if (shape == "topleft")
        {
            this["top"] = { color: color };
            this["left"] = { color: color };
        } else 
            this[shape] = { color: color };

        let firstPoint = null, secondPoint = null, thirdPoint = null;
        let halfSize = Math.ceil(this.constructor.size / 2);
        let ctx = this.ctx;
            ctx.beginPath();
            ctx.fillStyle = color;
            ctx.strokeStyle = color;
            ctx.lineWidth = 1;
        if (shape == "circle") {
            ctx.arc(this.start.x + halfSize, this.start.y + halfSize, halfSize - 1, 0, 2 * Math.PI);
            ctx.fill();
        }
        else if (shape == "square") {
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
                case "topleft": {
                    firstPoint = new Point(this.start.x, this.start.y);
                    secondPoint = new Point(this.end.x, this.start.y);
                    thirdPoint = new Point(this.start.x, this.end.y);
                    break;
                }
                case "bottomright": {
                    firstPoint = new Point(this.start.x, this.end.y);
                    secondPoint = new Point(this.end.x, this.end.y);
                    thirdPoint = new Point(this.end.x, this.start.y)
                    break;
                }
            }
            if (this.ctx != null) {
                ctx.moveTo(firstPoint.x, firstPoint.y);
                ctx.lineTo(secondPoint.x, secondPoint.y);
                ctx.lineTo(thirdPoint.x, thirdPoint.y);
                ctx.fill();
            }
        }
    }
}
Square.size = 80; // size in pixels of grid square
Square.widthEnd = null; // defines the horizontal end of coordinate system
Square.heightEnd = null; // defines the vertical end of coordinate system
Square.colors = []; // color pallet used in drawing
Square.takenSpace = []; // marks taken spots
Square.circleChance = 0; // chance of drawing a circle element
Square.inheritColorChance = 1; // chance of inhereting color of previous element