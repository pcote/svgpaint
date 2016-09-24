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


    var loginHandler = function(evt){

        var loginResult = function(res){
            if(res.state === "succeeded"){
                window.location = res.url;
            }
            else{
                alert("login failed");
            }
        };

        evt.preventDefault();
        var uname = $("#usernameTF").val();
        var pw = $("#passwordTF").val();
        var authString = "Basic " + btoa(uname + ":" + pw);

        var req = {
            url: "/login",
            method: "post",
            headers: {
                "Authorization": authString
            }
        };

        var promise = $.ajax(req);
        promise.then(loginResult);
    };

    $("#createuserButton").click(newUserHandler);
    $("#loginButton").click(loginHandler);
});