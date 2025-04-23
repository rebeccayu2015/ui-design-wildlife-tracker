$(document).ready(function () {
    $(".feedback").empty()
    $(".suspect-card").on("click", function () {
        let id = $(this).attr("id");

        if (id == 1) {
            window.location.href = "/quiz-result";
        } else {
            $(".feedback").append("Sorry. You selected the wrong suspect!");
            $('.btn').removeClass('d-none');
        }
    })
});