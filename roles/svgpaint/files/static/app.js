$(function(){
    var svg = SVG("drawingArea").size(800, 800);

    var dragging = false;
    var brushSize = 10;
    var currentColor = "#000000";

    /////////////// Routines for drawing in the drawing area ///////////////
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

    ///////////////// end routines for drawing in the drawing area ////////////

    ////////////////routines for loading and saving data //////////////////

    var saveClickHandler = function(evt){
        var svgData = $("#drawingArea")[0].children[0];
        var shapeOb = {};
        var recOb = {};
        var saveData = [];
        var i;
        var jsonArg;

        for(i=0; i < svgData.children.length; i++){
            shapeOb = svgData.children[i];

            recOb = {
                name: shapeOb.tagName,
                size: shapeOb.getAttribute("width"),
                x: shapeOb.getAttribute("x"),
                y: shapeOb.getAttribute("y"),
                color: shapeOb.getAttribute("fill")
            };

            saveData = saveData.concat(recOb);
        }

        jsonArg = {"saveData": saveData};

        var req = {
            url: "/save",
            method: "post",
            headers: {
                "Content-type": "application/json"
            },
            data: JSON.stringify(jsonArg)
        };


        var successCallback = function(data){
            alert(data);
        };

        var promise = $.ajax(req);
        promise.then(successCallback);
    };

    $("#menuSave").click(saveClickHandler);

});
