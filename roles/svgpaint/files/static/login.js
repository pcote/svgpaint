$(function(){

    var newUserHandler = function(evt){
        var newUsername = $("#newusernameTF").val();
        var newPassword = $("#newpasswordTF").val();
        var confirmedPassword = $("#confirmedpasswordTF").val();
        var jsonOb = {
            "newUsername": newUsername,
            "newPassword": newPassword,
            "confirmedPassword": confirmedPassword
        };


        var req = {
            url: "/createuser",
            method: "post",
            headers: {
                "Content-type": "application/json"
            },
            data: JSON.stringify(jsonOb)
        };

        var createUserCallback = function(res){
            alert(res);
        };

        var promise = $.ajax(req);
        promise.then(createUserCallback);
    };

    $("#createuserButton").click(newUserHandler);
});