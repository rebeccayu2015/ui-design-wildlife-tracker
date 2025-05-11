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
                if (correct_matches == 6 && total_number == 6) {
                    $("#sort-prints-feedback").text("Great job! You matched all " + correct_matches + "/" + total_number + " prints correctly. Click next to continue.");
                    $(".next-btn").removeClass('d-none')
                    $(".next-btn").addClass('d-block')
                }
                else{ 
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
        revert: "invalid",
        zIndex: 1000,
    });

    $(".family-box").droppable({
        accept: ".suspect-track",
        drop: function (event, ui) {
            $(this).append(ui.draggable);

            ui.draggable.css({
                top: '0px',
                left: '0px',
                position: 'relative' // or 'static' depending on your layout
            });
        
        }
    });
});