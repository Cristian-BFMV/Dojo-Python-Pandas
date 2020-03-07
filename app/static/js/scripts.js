function plot_graph(graph_json, chart_div) {
    var graphs = graph_json;
    //Plotly.react(chart_div, graphs, {});
    Window.Plotly.react(chart_div, graphs, {});
    var myPlot = document.getElementById(chart_div);
    if (myPlot) {
        myPlot.on('plotly_click', function (data) {
            var filter_name = data.points[0]['x'];
            var selected_date = $('#init_date').val();
            var post_data = {filter_name: filter_name, selected_date: selected_date, selected_chart: chart_div};
            $.post('/' + environment + '/alerts_table', post_data, function (data) {
                $('#alerts_table_div').html(data);
                $('#user_alerts_modal').modal('show');
            }).fail(function(response) {
                window.location.href = '/' + environment + '/home';
            });
        });
    }
}

function show_loading() {
    $("#submit").prop('disabled', true);
    $('#loading_message').show()
    $('.loader').show()
    return;
}

$('input[type=radio][name=upload_type]').change(function() {
    if (this.value == 'date_selection') {
        $('#load_by_date_div').show();
    } else {
        $('#load_by_date_div').hide();
    }
    if (this.value == 'daily' || this.value == 'date_selection') {
        $('#alerts_to_run').show();
    } else {
        $('#alerts_to_run').hide();
    }
});

$('input[type=radio][name=constant_alert_date]').change(function() {
    if (this.value == 'until_alert_date') {
        $('#constant_alert_date_div').show();
    } else {
        $('#constant_alert_date_div').hide();
    }
});


$('#init_date').datepicker({
    format: "dd/mm/yyyy",
    todayBtn: "linked",
    language: "es",
    autoclose: true
});

$('#alerts_date').datepicker({
    format: "dd/mm/yyyy",
    todayBtn: "linked",
    language: "es",
    autoclose: true
});

window.setTimeout(function() {
    $(".alert").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
    });
}, 4000);

$('.custom-file-input').on('change',function(){
    //get the file name
    let fileName = $(this).val().split('\\').pop();
    //replace the "Choose a file" label
    $(this).next('.custom-file-label').html(fileName);
});

$( document ).ready(function() {

    setInterval(function() {
        $.ajax({
            type: "post",
            url: '/' + environment + '/check_session',
            success:function(data) {
                console.log("ok");
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                window.location.href = '/' + environment + '/home';
            }
        });
    }, 3900000); //65 min

    $('#daily_load_form').submit(function(e) {
        $("#submit").prop('disabled', true);
        return;
    });

    $('#alert_comment_form').submit(function(e) {
        $("#comment_submit").prop('disabled', true);
        return;
    });

    $('#close_alert_form').submit(function(e) {
        $("#close_alert_submit").prop('disabled', true);
        return;
    });

    $('#init_date').change(function () {
        var selected_date = $(this).val();
        $.getJSON('/' + environment + '/dashboard_json', {selected_date: selected_date}, function(data) {
            var general_alerts_json = JSON.parse(data['general_alerts_json']);
            var alerts_by_management_json = JSON.parse(data['alerts_by_management_json']);
            var alerts_by_risk_json = JSON.parse(data['alerts_by_risk_json']);
            var alerts_by_user_json = JSON.parse(data['alerts_by_user_json']);
            plot_graph(general_alerts_json, 'total_alerts');
            plot_graph(alerts_by_risk_json, 'criticality_alerts');
            plot_graph(alerts_by_management_json, 'management_alert');
            plot_graph(alerts_by_user_json, 'users_alerts');
        })
    });

    $('#search_history_form').submit(function(e) {
        e.preventDefault();
        var account_id = $('#filter_account_id').val();
        var alerts_date = $('#alerts_date').val()
        var post_data = {account_id: account_id, alerts_date:alerts_date};
        $.post('/' + environment + '/filter_history', post_data, function (data) {
            $('#alerts_list_table').html(data);
        });
    });

    $('#reset_filters').click(function() {
        $('#filter_account_id').selectpicker('val', 'Todas');
        $('#alerts_date').val('');
        var account_id = $('#filter_account_id').val();
        var alerts_date = $('#alerts_date').val()
        var post_data = {account_id: account_id, alerts_date:alerts_date};
        $.post('/' + environment + '/filter_history', post_data, function (data) {
            $('#alerts_list_table').html(data);
        });
    });

    var info = '';
    var valueJson = '';
    if (document.getElementById("total_alerts_info") != null) {
        info = document.getElementById("total_alerts_info").value;
        valueJson = JSON.parse(info);
        plot_graph(valueJson, 'total_alerts');
    }

    if (document.getElementById("criticality_alerts_info") != null) {
        info = document.getElementById("criticality_alerts_info").value;
        valueJson = JSON.parse(info);
        plot_graph(valueJson, 'criticality_alerts');
    }

    if (document.getElementById("users_alerts_info") != null) {
        info = document.getElementById("users_alerts_info").value;
        valueJson = JSON.parse(info);
        plot_graph(valueJson, 'users_alerts');
    }

    if (document.getElementById("management_alert_info") != null) {
        info = document.getElementById("management_alert_info").value;
        valueJson = JSON.parse(info);
        plot_graph(valueJson, 'management_alert');
    }

    if (document.getElementById("accounts_behavior_info") != null) {
        info = document.getElementById("accounts_behavior_info").value;
        valueJson = JSON.parse(info);
        plot_graph(valueJson, 'accounts_behavior');
    }
    var classname = document.getElementsByClassName("btn-dialog");
    for (var i = 0; i < classname.length; i++) {
        classname[i].addEventListener('click', function(e){
            view_dialog($(e.target).data("myval"), 0)
        }, false);
    }

});

function comment_ajax(href) {
    var myObj = {};
    myObj['comment_text'] = document.getElementById("text_area_alert_comment").value;
    myObj['original_date'] = document.getElementById("original_date_comment").value;
    myObj['account_id'] = document.getElementById("account_id_comment").value;
    myObj['alert_type'] = document.getElementById("alert_type_comment").value;
    myObj['page'] = document.getElementById("page").value;
    myObj['original_alert_value'] = document.getElementById("original_alert_value_comment").value;
    var checked = 'undefined';
    if(document.getElementById("until_alert_date_radio") != null) {
        if(document.getElementById("until_alert_date_radio").checked) {
            checked = 'until_alert_date';
        }
    }
    if(document.getElementById("undefined_alert_date_radio") != null) {
        if(document.getElementById("undefined_alert_date_radio").checked) {
            checked = 'undefined_alert_date';
        }
    }
    if(document.getElementById("na_constant_alert_date_radio") != null) {
        if(document.getElementById("na_constant_alert_date_radio").checked) {
            checked = 'na';
        }
    }

    myObj['constant_alert_date'] = checked;
    if(document.getElementById("alerts_date") != null) {
        myObj['alerts_date'] = document.getElementById("alerts_date").value;
    }
    var origin   = window.location.origin;
    var pathname = window.location.pathname;
    var res = pathname.split("/");
    var environment = res[1];

    var post_data = myObj;
    $.post(origin+'/'+environment+'/comment', post_data, function (data) {
        document.getElementById("myModalFather").innerHTML='<div class="modal fade" id="myModal" role="dialog"><div class="modal-body" id="myModalClass"></div></div>';
        $('#myModal').modal('hide');
        $('body').removeClass('modal-open');
        $('body').removeAttr('style');
        $('.modal-backdrop').remove();
        view_dialog(href, 1);
    });

}

function view_dialog(href, comment_recently) {
    $('#myModal').modal({
        'show': true
    }).find('.modal-body').load(href, function (e) {
        var classnameb = document.getElementsByClassName("btn-modal-bootstrap");
        for (var i = 0; i < classnameb.length; i++) {
            classnameb[i].addEventListener('click', function(e){

                document.getElementById("myModalFather").innerHTML='<div class="modal fade" id="myModal" role="dialog"><div class="modal-body" id="myModalClass"></div></div>';
                $('#myModal').modal('hide');
                $('body').removeClass('modal-open');
                $('body').removeAttr('style');
                $('.modal-backdrop').remove();
                if(comment_recently == 1) {
                    var pathname = window.location.pathname;
                    var res = pathname.substring(0, pathname.length-1);
                    show_loading();

                    $.ajax({
                        url: res+'1',
                        type: 'get',
                        success: function (data) {
                            document.getElementById("modal-alerts-list").innerHTML=data;
                            var classname = document.getElementsByClassName("btn-dialog");
                            for (var i = 0; i < classname.length; i++) {
                                classname[i].addEventListener('click', function(e){
                                    view_dialog($(e.target).data("myval"), 0)
                                }, false);
                            }
                            $('#loading_message').hide()
                            $('.loader').hide()
                            $('input[type=radio][name=pending_check]').change(function () {
                                var pending_check = this.value;
                                var post_data = {pending_check: pending_check};
                                $.post('/' + environment + '/user_alerts_table', post_data, function (data) {
                                    $('#alerts_list_table').html(data);
                                });
                            });
                        },
                        error: function(e) {
                            $('#loading_message').hide()
                            $('.loader').hide()
                            alert('Se produjo un error, por favor contacte al administrador del sistema.');
                            console.log(e);
                        }
                    });
                }

            }, false);
        }
        var alertGraph = JSON.parse(document.getElementById("textHiden").value);
        plot_graph(alertGraph, 'accounts_behavior');
        if(document.getElementById("textHiden2").value == 'until_date') {
            $('#constant_alert_date_div').show();
        }
        document.getElementById("comment_submit_modal").addEventListener('click', function(e){ comment_ajax(href); }, false);


    });
}

$('input[type=radio][name=pending_check]').change(function () {
    var pending_check = this.value;
    var post_data = {pending_check: pending_check};
    $.post('/' + environment + '/user_alerts_table', post_data, function (data) {
        $('#alerts_list_table').html(data);
        var classname = document.getElementsByClassName("btn-dialog");
        for (var i = 0; i < classname.length; i++) {
            classname[i].addEventListener('click', function(e){
                view_dialog($(e.target).data("myval"), 0)
            }, false);
        }
    });
});

$('#select_account_id').change(function () {
    var account_id = $(this).val();
    $.getJSON('/' + environment + '/time_line/' + account_id, function(data) {
        plot_graph(data, 'accounts_behavior');
    })
});

$('#original_atypical_value').keypress(function () {
    var ex = /^[0-9]+\.?[0-9]*$/;
    var valor = $('#original_atypical_value').val();
    if(ex.test(valor)==false){
        $('#original_atypical_value').val(valor.substring(0,valor.length - 1));
        alert("Debe ingresar solo números, intente de nuevo.");
    }
});

$('#original_zero_value').keypress(function () {
    var ex = /^[0-9]+\.?[0-9]*$/;
    var valor = $('#original_zero_value').val();
    if(ex.test(valor)==false){
        $('#original_zero_value').val(valor.substring(0,valor.length - 1));
        alert("Debe ingresar solo números, intente de nuevo.");
    }
});
