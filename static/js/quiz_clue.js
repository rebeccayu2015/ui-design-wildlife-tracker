$(document).ready(function () {
    $(".feedback").empty()
    $(".suspect-card").on("click", function () {
        let id = $(this).attr("id");

        if (id == 1) {
            window.location.href = "/quiz-result";
        } else {
            $(".feedback").empty();
            $(".feedback").append("Sorry. You framed the wrong suspect!");
            $(".try-again-btn").removeClass('d-none')
            $(".try-again-btn").addClass('d-block')
            $(".clue-suspect-card").addClass('disabled')
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

    $(".try-again-btn").on("click", function () {
        $(".try-again-btn").removeClass('d-block')
        $(".try-again-btn").addClass('d-none')
        $(".feedback").empty();
        $(".clue-suspect-card").removeClass('disabled')
    });

    $(".clue-btn").on("click", function () {
        $.ajax({
            type: "POST",
            url: "/clue",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            success: function (result) {
                console.log("Success");
                clues = parseInt(result['clues'])
                clues_data = result['clues_data']

                $(".clue").empty();
                if (clues <= 5) {
                    for (let i = 1; i <= clues; i++) {
                        $(".clue").append(`<div>${i}. ${clues_data[i + 10]['text']}<\div>`);
                    }
                }
                if (clues >= 5) {
                    $(".clue-btn").removeClass('d-block')
                    $(".clue-btn").addClass('d-none')
                    $(".clue").append(`<hr><h2>All clues revealed. Please choose a culprit!<\h2>`);
                }

                $(".try-again-btn").removeClass('d-block')
                $(".try-again-btn").addClass('d-none')
                $(".feedback").empty();
            },
            error: function (request, status, error) {
                console.log("Error");
                console.log(request);
                console.log(status);
                console.log(error);
            }
        });
        $(".clue-suspect-card").removeClass('disabled')
        $(".feedback").empty();
    });
});
