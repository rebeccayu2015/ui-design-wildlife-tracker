$(document).ready(function () {
    $(".sort-btn").on("click", function () {
    
        $(".family-box").each(function () {
            let familyId = $(this).attr("id");
            let family = familyId.split("-")[1];
            let suspects = [];
    
            $(this).find(".suspect-track").each(function () {
                let suspectId = $(this).attr("id");
                suspects.push(suspectId.split("-")[1]);
            });
    
            sort_prints_responses[family] = suspects;
        });
        console.log(sort_prints_responses);

        // send responses to server
        $.ajax({
            type: "POST",
            url: "/check_sort_prints",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(sort_prints_responses),
            success: function (response) {
                let correct_matches = response['correct_matches']   
                let total_number = response['total_number']
                if (correct_matches == total_number) { // TODO: add condition to make sure that total_number = total number of prints
                    $("#sort-prints-feedback").text("Great job! You matched all " + correct_matches + "/" + total_number + " prints correctly. Click next to continue.");
                    $(".next-btn").removeClass('d-none')
                    $(".next-btn").addClass('d-block')
                }
                else{ // TODO: add condition for case where not all the prints are sorted but all the sorted ones are correct
                    $("#sort-prints-feedback").text("You matched " + correct_matches + "/" + total_number + " prints correctly. Try again!");
                }
            },
            error: function (request, status, error) {
                console.log("Error");
                console.log(request);
                console.log(status);
                console.log(error);
            }
        });
    })

    $(".suspect-track").draggable({
        revert: true,
        zIndex: 1000,
    });

    $(".family-box").droppable({
        //accept: ".suspect-track",
        drop: function (event, ui) {
            $(this).append(ui.draggable);
        }
    });
});