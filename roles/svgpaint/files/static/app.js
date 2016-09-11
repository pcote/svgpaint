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


    var successMessage = function(msg){
        alert(msg);
    };

    var saveUserData = function(creds){
        var drawingData = []
        var rawSvgList = $("#drawingArea")[0].children[0].children;
        var drawingName = $("#drawingNameField").val();
        var i;
        var pixelRecord;
        var jsonData = "";

        for(i=0; i< rawSvgList.length; i++){
            tag = rawSvgList[i]
            if(tag.tagName === "rect" || tag.tagName === "circle"){
                pixelRecord = {
                    shape: tag.tagName,
                    color: tag.getAttribute("fill"),
                    x: tag.getAttribute("x"),
                    y: tag.getAttribute("y"),
                    size: tag.getAttribute("width")
                };

                drawingData = drawingData.concat(pixelRecord);
            }
        }

        jsonArg = JSON.stringify({
            "drawingData": drawingData,
            "drawingName": drawingName });

        var username = creds.username;
        var password = creds.password;
        var basicCreds = "Basic " + btoa(username + ":" + password);
        var req = {
            url: "/save",
            method: "post",
            headers: {
                "Content-type": "application/json",
                "Authorization": basicCreds
            },

            data: jsonArg
        };

        var promise = $.ajax(req)
        promise.then(successMessage);
    };

    var getUserCredentials = function(){
        var req = {
            url: "/usercreds",
            method: "get"
        };

        var promise = $.ajax(req);
        return promise;
    };

    var saveHandler = function(evt){
        var promise = getUserCredentials();
        promise.then(saveUserData);
    };

    $("#menuSave").click(saveHandler);
});