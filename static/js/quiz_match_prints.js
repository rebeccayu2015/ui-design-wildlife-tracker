$(document).ready(function () {
    $(".suspect-track").each(function () {
        $(this).data("originalParent", $(this).parent());
    });

    $(".match-btn").on("click", function () {
        $(".next-btn").removeClass('d-none')
        $(".next-btn").addClass('d-block')
    })

    $(".suspect-track").draggable({
        revert: true,
        cursor: "move",
        zIndex: 1000,
    });

    $(".empty-square").droppable({
        //accept: ".suspect-track",
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