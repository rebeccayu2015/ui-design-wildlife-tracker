$(document).ready(function () {
    $(".sort-btn").on("click", function () {
        $(".next-btn").removeClass('d-none')
        $(".next-btn").addClass('d-block')
    })

    $(".suspect-track").draggable({
        revert: true,
        cursor: "move",
        zIndex: 1000,
    });

    $(".family-box").droppable({
        //accept: ".suspect-track",
        drop: function (event, ui) {
            $(this).append(ui.draggable);
        }
    });
});