$(document).ready(function () {
    var district;
    var local_level;

    let entry_id = $('#entry_id').val();

    district  = $('#district_id').val();

    if(district){
        $.ajax({
            url: '/master/get-district-locallevel/'+entry_id,
            type: "GET",
            success: function (data) {
                debugger;
                district = data[0].district_id;
                local_level = data[0].local_level_id;
            }
        });
    }
    $.urlParam = function (name) {
        try {
            var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
            return results[1] || 0;
        } catch {
            return null;
        }
    }
    $('#district_id').empty().append('<option value="">--select province--</option>');
    $('#local_level_id').empty().append('<option value="">--select province--</option>');

    $('#id_province').on('change', function () {
        var stateID = $(this).val();
        $('#district_id').append('<option value="">-- Loading...  --</option>');

        if (stateID) {
            $.ajax({
                url: '/master/get-districts/' + stateID,
                type: "GET",
                dataType: "json",
                success: function (data) {

                    if (data) {
                        $('#district_id').empty().append('<option value="">-- select district  --</option>');
                        $('#local_level_id').empty().append('<option value="">--select district--</option>');
                        var selected_id = district;
                        $.each(data, function (key, value) {
                            var selected = "";
                            if (selected_id == value.id) {
                                selected = "SELECTED";
                            }
                            $('select[name="district"]').append('<option class="form-control" value="' + value.id + '" ' + selected + '>' + value.name_en + '</option>');
                            if (selected == "") {
                                $("#district_id").trigger("change");
                                $("#local_level_id").trigger("change");
                            }
                        });
                    } else {
                        $('#district_id').empty();
                        $('#local_level_id').empty();
                    }
                }
            });
        } else {
            $('#district_id').empty().append('<option value="">--select province--</option>');
            $('#local_level_id').empty().append('<option value="">--select province--</option>');
        }
    });

    $('#district_id').on('change', function () {
        var districtID = $(this).val();
        $('#local_level_id').empty().append('<option value="">--select local level--</option>');

        if (districtID) {
            $('#local_level_id').append('<option value="">-- Loading...  --</option>');
            $.ajax({
                url: '/master/get-local-levels/' + districtID,
                type: "GET",
                dataType: "json",
                success: function (data) {
                    if (data) {
                        $('#local_level_id').empty().append('<option value="">-- select local level --</option>');
                        var selected_id = local_level;
                        $.each(data, function (key, value) {
                            var selected = "";
                            if (selected_id == value.id) {
                                selected = "SELECTED";
                            }
                            $('select[name="local_level"]').append('<option class="form-control" value="' + value.id + '" ' + selected + '>' + value.name_en + '</option>');
                            if (selected == "") {
                                $("#local_level_id").trigger("change");
                            }
                        });
                    } else {
                        $('#local_level_id').empty();
                    }
                }
            });
        } else {
            $('#local_level_id').empty().append('<option value="">-- select local level --</option>');
        }
    });

    setTimeout(() => {
        $("#id_province").trigger("change");
    }, 500);
});


