$("#login-form").on("submit", function(e) {
    e.preventDefault();
    login($("#email").val(), $("#password").val());
});

function login(email, password) {
    $.post("/api/user/login", {
        email: email,
        password: password
    }, function(data) {
        $("#status").text(data.message);
        if (data.success == 1) {
            // wait then redirect or whatever
        }
    });
}
