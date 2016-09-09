$(function(){
    var svg = SVG("drawingArea").size(800, 800);

    var dragging = false;
    var brushSize = 10;
    var currentColor = "#000000";

    var mouseUpHandler = function(evt){
        dragging = false;
    };

    var mouseDownHandler = function(evt){
        dragging = true;
    };

    var mouseDrawHandler = function(evt){
        var currentShape = "square"; // default
        var xPos = evt.offsetX;
        var yPos = evt.offsetY;
        if(dragging){
            currentShape = $("#shapeSelect").val();
            if(currentShape === "square"){
                var shape = svg.rect(brushSize, brushSize);
            }
            else {
                var shape = svg.circle(brushSize);
            }
            shape.move(xPos, yPos);
            shape.fill(currentColor);
        }
    };

    var brushChangeHandler = function(evt){
        var newBrushSize = $("#brushSizeField").val();
        brushSize = Number(newBrushSize);
    };

    var colorChangeHandler = function(evt){
        currentColor = $("#colorInput").val();
    };

    var wipeClickHandler = function(evt){
        svg.clear();
    };

    $("#drawingArea").mousemove(mouseDrawHandler);
    $("#drawingArea").mouseup(mouseUpHandler);
    $("#drawingArea").mousedown(mouseDownHandler);
    $("#brushSizeField").change(brushChangeHandler);
    $("#colorInput").change(colorChangeHandler);
    $("#wipeButton").click(wipeClickHandler);
});