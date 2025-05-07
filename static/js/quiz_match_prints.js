$(document).ready(function () {
    $(".suspect-track").each(function () {
        $(this).data("originalParent", $(this).parent());
    });

    $(".match-btn").on("click", function () {
        responses = {}
        $(".empty-square").each(function () {
            let squareId = $(this).attr("id");
            let suspectId = $(this).find(".suspect-track").attr("id");
            if (suspectId != undefined) {
                match_prints_responses[squareId.split("-")[1]] = suspectId.split("-")[1];
            }
        })
        console.log(match_prints_responses);

        // send responses to server to get feedback
        $.ajax({
            type: "POST",
            url: "/check_match_prints",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(match_prints_responses),
            success: function (response) {
                console.log(response);
                let correctMatches = response['correct_matches']
                let totalNumber = response['total_number']
                if (correctMatches == totalNumber) { // TODO: move button appearance to this block
                    $("#match-prints-feedback").text("Great job! You matched all " + correctMatches + "/" + totalNumber + " prints correctly. Click next to continue.");
                    $(".next-btn").removeClass('d-none')
                    $(".next-btn").addClass('d-block')
                }
                else{ // TODO: add condition for case where not all the prints are sorted but all the sorted ones are correct
                    $("#match-prints-feedback").text("You matched " + correctMatches + "/" + totalNumber + " prints correctly. Try again!");
                }
            },
            error: function (request, status, error) {
                console.log("Error");
                console.log(request);
                console.log(status);
                console.log(error);
            }
        })
    })

    $(".suspect-track").draggable({
        revert: true,
        zIndex: 1000,
    });

    $(".empty-square").droppable({
        drop: function (event, ui) {
            let $square = $(this);
            let $newItem = ui.draggable;
            let $existingItem = $square.find(".suspect-track");
            if ($existingItem.length > 0) {
                let $originalParent = $existingItem.data("originalParent");
                $existingItem.detach().css({ top: 0, left: 0 }).appendTo($originalParent);
            }
            $newItem.detach().css({ top: 0, left: 0 }).appendTo($square);
        }
    });
});