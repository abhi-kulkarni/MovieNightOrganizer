$(document).on('show.bs.modal', '#addFriendsModal', function (e) {
    $('#add_friends_form_modal').trigger("reset");
    $("#first_name").removeClass("is-invalid");
    $("#last_name").removeClass("is-invalid");
    $("#first_name").removeClass("is-valid");
    $("#last_name").removeClass("is-valid");
    $("#first_name_error").hide();
    $("#last_name_error").hide();
});

$(document).on('show.bs.modal', '.edit_friends_modal', function (e) {
   
    let id = e.target.id.split("_")[1];
    $('#edit_friends_form_modal_'+id).trigger("reset");
    let first_name_ele = document.getElementById('first_name_'+id);
    let last_name_ele = document.getElementById('last_name_'+id);
    let first_name_error = document.getElementById('first_name_error_'+id);
    let last_name_error = document.getElementById('last_name_error_'+id);
    first_name_ele.classList.remove("is-invalid");
    last_name_ele.classList.remove("is-invalid");
    first_name_ele.classList.remove("is-valid");
    last_name_ele.classList.remove("is-valid");
    first_name_error.style.display = "none";
    last_name_error.style.display = "none";

    $("#first_name_"+id).on("change keyup paste", function(e){
        if(e.target.value.length <= 0){
            $("#first_name_"+id).removeClass("is-valid");
            $("#first_name_"+id).addClass("is-invalid");
            $("#first_name_error_"+id).show();
        }else{
            $("#first_name_"+id).removeClass("is-invalid");
            $("#first_name_"+id).addClass("is-valid");
            $("#first_name_error_"+id).hide();
        }
    })

    $("#last_name_"+id).on("change keyup paste", function(e){
        if(e.target.value.length <= 0){
            $("#last_name_"+id).removeClass("is-valid");
            $("#last_name_"+id).addClass("is-invalid");
            $("#last_name_error_"+id).show();
        }else{
            $("#last_name_"+id).removeClass("is-invalid");
            $("#last_name_"+id).addClass("is-valid");
            $("#last_name_error_"+id).hide();
        }
    })

});

$(document).on('show.bs.modal', '#addMoviesModal', function (e) {
    $('#add_movies_form_modal').trigger("reset");
    $("#movie_name").removeClass("is-invalid");
    $("#movie_name").removeClass("is-valid");
    $("#movie_name_error").hide();
});

$(document).on('show.bs.modal', '.edit_movies_modal', function (e) {
   
    let id = e.target.id.split("_")[1];
    $('#edit_movies_form_modal_'+id).trigger("reset");
    let movie_name_ele = document.getElementById('movie_name_'+id);
    let movie_name_error = document.getElementById('movie_name_error_'+id);
    movie_name_ele.classList.remove("is-invalid");
    movie_name_ele.classList.remove("is-valid");
    movie_name_error.style.display = "none";

    $("#movie_name_"+id).on("change keyup paste", function(e){
        if(e.target.value.length <= 0){
            $("#movie_name_"+id).removeClass("is-valid");
            $("#movie_name_"+id).addClass("is-invalid");
            $("#movie_name_error_"+id).show();
        }else{
            $("#movie_name_"+id).removeClass("is-invalid");
            $("#movie_name_"+id).addClass("is-valid");
            $("#movie_name_error_"+id).hide();
        }
    })

});


$(document).ready(function(){
    
    $("#messages").delay(5000).slideUp(300);

    if(window.location.pathname === '/'  || window.location.pathname.includes('movies')){
        $('#friends_tab').css({"color": "#0879FA"});
    }else if(window.location.pathname === '/organizer'){
        $('#organizer_tab').css({"color": "#0879FA"});
    }
    
    $('[data-toggle="popover"]').popover();

    $(".friends_table").fancyTable({
        pagination: true,
        sortable: false,
        perPage:5,
        searchable: false,
        globalSearch:false
    });		

    $(".movies_table").fancyTable({
        pagination: true,
        sortable: false,
        sortColumn:0,
        perPage:5,
        searchable: false,
        globalSearch:false
    });		
    
    $('[data-tooltip="tooltip"]').tooltip({
        placement : 'top'
    });

    $("#first_name").on("change keyup paste", function(e){
        if(e.target.value.length <= 0){
            $("#first_name").removeClass("is-valid");
            $("#first_name").addClass("is-invalid");
            $("#first_name_error").show();
        }else{
            $("#first_name").removeClass("is-invalid");
            $("#first_name").addClass("is-valid");
            $("#first_name_error").hide();
        }
    })

    $("#last_name").on("change keyup paste", function(e){
        if(e.target.value.length <= 0){
            $("#last_name").removeClass("is-valid");
            $("#last_name").addClass("is-invalid");
            $("#last_name_error").show();
        }else{
            $("#last_name").removeClass("is-invalid");
            $("#last_name").addClass("is-valid");
            $("#last_name_error").hide();
        }
    })


    $("#movie_name").on("change keyup paste", function(e){
        if(e.target.value.length <= 0){
            $("#movie_name").removeClass("is-valid");
            $("#movie_name").addClass("is-invalid");
            $("#movie_name_error").show();
        }else{
            $("#movie_name").removeClass("is-invalid");
            $("#movie_name").addClass("is-valid");
            $("#movie_name_error").hide();
        }
    })

});

function openAddFriendsModal(){
    $('#addFriendsModal').modal('show');
}

function openAddMoviesModal(){
    $('#addMoviesModal').modal('show');
}

function setSelectedUsers (){
    var friend_id_list = $(".friends_table input:checkbox:checked").map(function () {
        var checkbox_id = $(this)[0].id;
        var friend_id = checkbox_id.split("_")[1];
        return parseInt(friend_id);
    }).get();
    $('#selected_friends').val(friend_id_list);
}

$('#select_all_friends').change(function () {
    if($(this).prop('checked')){
        var friend_id_list = [];
        $('tbody tr td input[type="checkbox"]').each(function(){
            $(this).prop('checked', true);
            var checkbox_id = $(this)[0].id;
            var friend_id = checkbox_id.split("_")[1];
            friend_id_list.push(friend_id);
        });
    }else{
        $('tbody tr td input[type="checkbox"]').each(function(){
            $(this).prop('checked', false);
        });
    }
    if($(this).prop('checked')){
        $('#selected_friends').val(friend_id_list);
    }else{
        $('#selected_friends').val('selected_friends');
    }
});