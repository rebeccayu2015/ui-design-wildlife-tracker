$(document).ready(function () {
    $(".feedback").empty()
    $(".suspect-card").on("click", function () {
        let id = $(this).attr("id");

        if (id == 1) {
            window.location.href = "/quiz-result";
        } else {
            $(".feedback").empty();
            $(".feedback").append("Sorry. You selected the wrong suspect!");
            $('.btn').removeClass('d-none');
        }

        let data = {
            'answer': id
        }

        $.ajax({
            type: "POST",
            url: "/record_response",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(data),
            success: function (result) {
                console.log("Success");
            },
            error: function (request, status, error) {
                console.log("Error");
                console.log(request);
                console.log(status);
                console.log(error);
            }
        });
    })
});