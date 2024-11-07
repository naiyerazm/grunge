var BaseUrl = '/'

$(document).ready(function () {

    $('#btn-login').click(function () {
        $.ajax({
            type: 'POST',
            url: BaseUrl + 'user/login/',
            data: $('#frm-login').serialize(),
            dataType: "json",
            beforeSend: function () {
                $('.error').text();
            },
            success: function (response) {
                if (response.status_code == 400) {
                    $.each(response.errorList, function (index, val) {
                        $('#error-' + index).text(val);
                    });
                    alert(response.msg);
                }
                else {
                    window.location = BaseUrl + 'user/artist/list'
                }
                if (response.status_code == 500) {
                    alert(response.msg);
                }
            }
        });
        return false;
    });

    $('#btn-save-artist').click(function () {
        $.ajax({
            type: 'POST',
            url: BaseUrl + 'user/artist/',
            data: $('#frmArtist').serialize(),
            dataType: "json",
            beforeSend: function () {
                $('#error').hide();
            },
            success: function (response) {
                if (response.status_code == 400) {
                        $('#error').text(response.msg);
                        $('#error').show();
                }
                else {
                    window.location = BaseUrl + 'user/artist/list'
                }
                if (response.status_code == 500) {
                    $('#error').text(response.msg);
                    $('#error').show();
                }
            }
        });
        return false;
    });

    $('#btn-save-album').click(function () {
        $.ajax({
            type: 'POST',
            url: BaseUrl + 'user/album/',
            data: $('#frmAlbum').serialize(),
            dataType: "json",
            beforeSend: function () {
                $('#error').hide();
            },
            success: function (response) {
                if (response.status_code == 400) {
                    $('.error').show();
                    $.each(response.errors, function(i, item) {
                        $('#frmAlbum #'+i+'-error').text(item);
                 });
                }
                else {
                    window.location = BaseUrl + 'user/album/list'
                }
                if (response.status_code == 500) {
                    $('#error').text(response.msg);
                    $('#error').show();
                }
            }
        });
        return false;
    });


    $('#btn-save-track').click(function () {
        $.ajax({
            type: 'POST',
            url: BaseUrl + 'user/track/',
            data: $('#frmTrack').serialize(),
            dataType: "json",
            beforeSend: function () {
                $('#error').hide();
            },
            success: function (response) {
                if (response.status_code == 400) {
                    $('.error').show();
                    $.each(response.errors, function(i, item) {
                        $('#frmTrack #'+i+'-error').text(item);
                 });
                }
                else {
                    window.location = BaseUrl + 'user/track/list'
                }
                if (response.status_code == 500) {
                    $('#error').text(response.msg);
                    $('#error').show();
                }
            }
        });
        return false;
    });

    $('#btn-save-playlist').click(function () {
        $.ajax({
            type: 'POST',
            url: BaseUrl + 'user/playlist/',
            data: $('#frmPlaylist').serialize(),
            dataType: "json",
            beforeSend: function () {
                $('#error').hide();
            },
            success: function (response) {
                if (response.status_code == 400) {
                    $('.error').show();
                    $.each(response.errors, function(i, item) {
                        $('#frmPlaylist #'+i+'-error').text(item);
                 });
                }
                else {
                    window.location = BaseUrl + 'user/playlist/list'
                }
                if (response.status_code == 500) {
                    $('#error').text(response.msg);
                    $('#error').show();
                }
            }
        });
        return false;
    });
    
    $('#btnAddTrack').click(function(){
        var html = '<div class="form-group row">'+$('#track-div').html()+'<div class="col-sm-1 "><a name="btnRemoveTrack" class="btn-remove-track" href="javascript:void(0)"><i class="material-icons">&#xe872;</i></a></div></div>'
        $(html).insertAfter('#track-div');
        return false;
    });

    $(document).on('click', '.btn-remove-track', function(){
        $(this).parent().parent().remove();
    });

    $('#btnAddPlaylistTrack').click(function(){
        var html = '<div class="form-group row">'+$('#playlist-track-div').html()+'<div class="col-sm-1 "><a name="btnRemovePlaylistTrack" class="btn-remove-playlist-track" href="javascript:void(0)"><i class="material-icons">&#xe872;</i></a></div></div>'
        $(html).insertAfter('#playlist-track-div');
        return false;
    });

    $(document).on('click', '.btn-remove-playlist-track', function(){
        $(this).parent().parent().remove();
    });

});

function get_artist_info(id){
    $.ajax({
        type: 'get',
        url: BaseUrl + 'user/artist/get-artist/' + id,
        dataType: "json",
        success: function (response) {
            $('#form-title').text('Edit Artist');
            $('#frmArtist #uuid').val(response.artist_info.uuid);
            $('#frmArtist #name').val(response.artist_info.name);
        }
    });
}

function get_album_info(id){
    $.ajax({
        type: 'get',
        url: BaseUrl + 'user/album/get-album/' + id,
        dataType: "json",
        success: function (response) {
            $('#form-title').text('Edit Album');
            $('#frmAlbum #uuid').val(response.album_info.uuid);
            $('#frmAlbum #name').val(response.album_info.name);
            $('#frmAlbum #year').val(response.album_info.year);
            $('#frmAlbum #artist').val(response.album_info.artist.uuid);
            j = 1;
            $(".track-div").each(function() {
                if(j > 1){
                    $(this).remove();
                }
                j++;
            });
            j = 1;
            $.each(response.album_info.tracks, function(i, track) {
                if(j == 1){
                    $('#frmAlbum #track-1').val(track.name);
                    $('#frmAlbum #track-number-1').val(track.number);
                }
                else{
                    var html = '<div class="form-group row track-div">'+$('#track-div').html()+'<div class="col-sm-1 "><a name="btnRemoveTrack" class="btn-remove-track" href="javascript:void(0)"><i class="material-icons">&#xe872;</i></a></div></div>';
                    html = html.replace("track-1", "track-"+j);
                    html = html.replace("track-number-1", "track-number-"+j);
                    $(html).insertAfter('#track-div');
                    $('#track-'+j).val(track.name);
                    $('#track-number-'+j).val(track.number);
                }
                j++;
         });
        }
    });
}

function get_track_info(id){
    $.ajax({
        type: 'get',
        url: BaseUrl + 'user/track/get-track/' + id,
        dataType: "json",
        success: function (response) {
            $('#form-title').text('Edit Track');
            $('#frmTrack #uuid').val(response.track_info.uuid);
            $('#frmTrack #name').val(response.track_info.name);
            $('#frmTrack #number').val(response.track_info.number);
            $('#frmTrack #album').val(response.track_info.album.uuid);
        }
    });
}

function get_playlist_info(id){
    $.ajax({
        type: 'get',
        url: BaseUrl + 'user/playlist/get-playlist/' + id,
        dataType: "json",
        success: function (response) {
            $('#form-title').text('Edit Playlist');
            $('#frmPlaylist #uuid').val(response.playlist_info.uuid);
            $('#frmPlaylist #name').val(response.playlist_info.name);
            j = 1;
            $(".playlist-track-div").each(function() {
                if(j > 1){
                    $(this).remove();
                }
                j++;
            });
            j = 1;
            $.each(response.playlist_info.tracks, function(i, track) {
                if(j == 1){
                    $('#frmPlaylist #track-1').val(track.track.uuid);
                }
                else{
                    var html = '<div class="form-group row playlist-track-div">'+$('#playlist-track-div').html()+'<div class="col-sm-1 "><a name="btnRemovePlaylistTrack" class="btn-remove-playlist-track" href="javascript:void(0)"><i class="material-icons">&#xe872;</i></a></div></div>';
                    html = html.replace("track-1", "track-"+j);
                    $(html).insertAfter('#playlist-track-div');
                    $('#frmPlaylist #track-'+j).val(track.track.uuid);
                }
                j++;
         });
        }
    });
}

function delete_module(uuid,module_type) {
    if (!confirm('Are you sure to delete the record?')) {
        return false;
    }
    $.ajax({
        type: 'delete',
        url: BaseUrl + 'user/'+module_type+'/' + uuid,
        dataType: "json",
        success: function (response) {
            if (response.status_code == 400) {
                alert(response.msg);
            }
            else if (response.status_code == 500) {
                alert(response.msg);
            }
            else {
                window.location = BaseUrl + 'user/'+module_type+'/list'
            }

        }
    });
}