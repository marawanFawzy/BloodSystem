// Sidebar
var sidebar_is_shown = false;
var open = true
var filled = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

// Sections
$('page .page-header ul li').click(function () {
  if ($(this).hasClass('disabled'))
    return;
  var page = $(this).parent().parent().parent();
  $('section.active', page).removeClass('active');
  $('.page-header ul li', page).removeClass('active');
  $('section#' + $(this).data('target-section'), page).addClass('active');
  $(this).addClass('active');
  $('.page-header span', page).html($(this).html());
  $('section#' + $(this).data('target-section'), page).trigger('load');
})

//button
$('section#out button').click(function () {
  var button = $(this).parent().parent().parent();
  $('button.active', button).addClass(' ');
  $('button.active', button).removeClass('active');
  $('button#' + $(this).data('target-section'), button).addClass('active');
  $(this).addClass('active');
  $('.feedback').html('');
})

// Forms
jQuery.fn.extend({
  disable: function (state) {
    return this.each(function () {
      this.disabled = state;
    });
  }
});

function clearForm(form) {
  $('input[type="text"], input[type="number"], select', form).val('');
  $('input[type="radio"]', form).prop('checked', false);
  $('input[type="checkbox"]', form).prop('checked', false);
  $('textarea', form).val('');
  $('input[name="action"]').val('insert');
  Currently_edit = 0;
  return;
}

$("form").submit(function (e) {
  var form = $(this);
  var request = {
    url: form.attr('action'),
    type: form.attr('method'),
    data: form.serialize(),
    success: function (response) {
      $('.feedback', form).html(response);
    },
    error: function () {
      $('.feedback', form).html('<span class="error">Unexpected error or server is down</span>');
    },
    complete: function (jqXHR, textStatus) {
      clearForm(form);
      $('input, textarea, select, button', form).disable(false);
      $('input', form).eq(0).focus();

      if ($('page#pharmacy').hasClass('active') && $('section#patients').hasClass('active')) {
        filled = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        $('page#pharmacy section#patients input[name="action"]').val('insert');
        $('page#pharmacy section#patients tbody').html('<tr><td><select id="drugs-0" name="drugs-0" autocomplete="on" onclick="fill(0)"></select></td><td><input type="number" name="qty-0" autocomplete="off"></td><!--<td><button type="button" class="btn btn-success btn-sm" onclick="dispense(this)"><i class="fa fa-check"></i></button></td></tr>');
        $('page#pharmacy section#patients table select').on('input', pharmacyCheckDrugs);
        $('#ph_patients_feedback').html('');
        $('input#ph_code').focus();
      }
    }
  }
  $('.feedback', form).html('<div class="loader"><div class="scanner"><span>Loading...</span></div></div>');
  $('input, textarea, select, button', form).disable(true);
  $.ajax(request);
  return false;
});
function update_value(lab_code, value, filter) {
  if (value === "")
    alert("please fill the value of lab code (" + lab_code + ") first");
  else {
    setTimeout(function () {
      $.ajax({
        url: '/blood/out',
        type: 'GET',
        data: { 'filter': filter, 'lab_code': lab_code, 'value': value },
        success: function (response) {
          $('section#out div span.feedback').html(response);
          if (!response.includes("Error")) {
            q = "row-" + lab_code
            document.getElementById(q).innerText = ''
          }
        },
        error: function (response) {
          $('section#out div span.feedback').html(response);
        },
      });
    }, 0);
  }
}
function filter(filter) {
  $('page#blood section#out table#data tbody').html('');
  $('section#out div span.feedback').html('<div class="loader"><div class="scanner"><span>Loading...</span></div></div>');
  $.ajax({
    url: '/blood/filter',
    type: 'GET',
    data: { 'filter': filter },
    success: function (response) {
      var count = 0;
      data = JSON.parse(unescape(response));
      data.forEach(function (x) {
        count += 1;
        lab_code = x[00];
        row = "<tr id=row-" + lab_code + "  ><td><form class=\"form-out\">";
        row += "<h3 style=\"margin-left: 10px; min-width:80px\">" + lab_code + "</h3>"
        row += "<input class=\"form-control form-out-element input left\" id=" + lab_code + " autocomplete=\"off\" type=\"text\" required>";
        row += "<button type=\"button\" class=\"button form-control form-out-element right\" onclick=\"setTimeout(function () {update_value('" + lab_code + "', document.getElementById('" + lab_code + "').value , '" + filter + "')},200)\">update</button>"
        //row += "<button type=\"button\" class=\"form-control form-out-element\" onclick=\"update_value('" + lab_code + "', document.getElementById('" + lab_code + "').value , '" + filter + "')\">update</button>";
        row += "</form></td></tr>"

        $('page#blood section#out table#data tbody').append(row);
      })
      $('section#out div span.feedback').html('');
    },
    error: function () {
      $('section#out div span.feedback').html('Server Error');
    },
  });
}
function refreshBloodSheet() {
  $('page#blood section#sheet table tbody').html('');
  $.ajax({
    url: '/blood/sheet',
    type: 'GET',
    data: '',
    success: function (response) {
      var count = 0;
      data = JSON.parse(unescape(response));
      data.forEach(function (x) {
        count += 1;
        lab_code = x[00];
        sheet_code = x[01];
        in_time = x[02];
        tests = x[04];
        tubes = x[05];
        out_time = x[09];
        hepatitis = x[11];
        cbc = x[12];
        albumin = x[13];
        gpt = x[14];
        pt = x[15];
        bilirubin_direct = x[16];
        bilirubin_total = x[17];
        creatinine = x[18];
        urea = x[19]
        uric = x[20];
        glucose = x[21];
        esr = x[22];
        tag = x[23];
        hba1c = x[24];
        Total_cholesterol = x[25];
        _2Hpp = x[26];
        asot = x[27];
        crp = x[28];
        ldl = x[29];
        hdl = x[30];
        var res = "";
        var show = "";
        var flag = false;
        for (let i = 11; i < 31; i++) {
          if (x[i] != -10 && x[i] != -1) {
            if (i == 11) searchfor = "Hepatitis"
            else if (i == 12) searchfor = "CBC"
            else if (i == 13) searchfor = "Albumin"
            else if (i == 14) searchfor = "GPT"
            else if (i == 15) searchfor = "PT"
            else if (i == 16) searchfor = "Bilirubin_direct"
            else if (i == 17) searchfor = "Bilirubin_total"
            else if (i == 18) searchfor = "Creatinine"
            else if (i == 19) searchfor = "Urea"
            else if (i == 20) searchfor = "Uric"
            else if (i == 21) searchfor = "Glucose"
            else if (i == 22) searchfor = "ESR"
            else if (i == 23) searchfor = "TAG"
            else if (i == 24) searchfor = "HBA1C"
            else if (i == 25) searchfor = "Total_cholesterol"
            else if (i == 26) searchfor = "2Hpp"
            else if (i == 27) searchfor = "ASOT"
            else if (i == 28) searchfor = "CRP"
            else if (i == 29) searchfor = "LDL"
            else if (i == 30) searchfor = "HDL"

            result = tests.indexOf(searchfor)
            res = tests.substring(0, result) + '<span style="color: #6cbe45; font-weight: bold">' + tests.substring(result, result + searchfor.length) + "</span>" + tests.substring(result + searchfor.length);
            tests = res
            flag = true;
          }
        }
        for (let i = 11; i < 31; i++) {
          if (x[i] != -10) {
            if (i == 11) show += "Hepatitis = " + (hepatitis != -1 ? hepatitis : " ") + "\n"
            else if (i == 12) show += "CBC = " + (cbc != -1 ? cbc : " ") + "\n"
            else if (i == 13) show += "Albumin = " + (albumin != -1 ? albumin : " ") + "\n"
            else if (i == 14) show += "GPT = " + (gpt != -1 ? gpt : " ") + "\n"
            else if (i == 15) show += "PT = " + (pt != -1 ? pt : " ") + "\n"
            else if (i == 16) show += "Bilirubin_direct = " + (bilirubin_direct != -1 ? bilirubin_direct : " ") + "\n"
            else if (i == 17) show += "Bilirubin_total = " + (bilirubin_total != -1 ? bilirubin_total : " ") + "\n"
            else if (i == 18) show += "Creatinine = " + (creatinine != -1 ? creatinine : " ") + "\n"
            else if (i == 19) show += "Urea = " + (urea != -1 ? urea : " ") + "\n"
            else if (i == 20) show += "Uric = " + (uric != -1 ? uric : " ") + "\n"
            else if (i == 21) show += "Glucose = " + (glucose != -1 ? glucose : " ") + "\n"
            else if (i == 22) show += "ESR = " + (esr != -1 ? esr : " ") + "\n"
            else if (i == 23) show += "TAG = " + (tag != -1 ? tag : " ") + "\n"
            else if (i == 24) show += "HBA1C = " + (hba1c != -1 ? hba1c : " ") + "\n"
            else if (i == 25) show += "Total_cholesterol = " + (Total_cholesterol != -1 ? Total_cholesterol : " ") + "\n"
            else if (i == 26) show += "2Hpp = " + (_2Hpp != -1 ? _2Hpp : " ") + "\n"
            else if (i == 27) show += "ASOT = " + (asot != -1 ? asot : " ") + "\n"
            else if (i == 28) show += "CRP = " + (crp != -1 ? crp : " ") + "\n"
            else if (i == 29) show += "LDL = " + (ldl != -1 ? lab_code : " ") + "\n"
            else if (i == 30) show += "HDL = " + (hdl != -1 ? hdl : " ") + "\n"

          }
        }
        if (!flag)
          res = tests;

        show += "sheet code = " + sheet_code
        row = '<tr><td>' + count + '</td><td>' + lab_code + '</td><td>' + in_time + '</td><td>' + out_time + '</td><td>' + tubes + '</td><td>' + res + '</td>';
        row += '<td><button style="min-width:60px" onclick="setTimeout(function () {alert(\`' + show + '\`)},300);">results</button></td></tr>';
        $('page#blood section#sheet table tbody').append(row);
      })
    },
    error: function () {
      alert('Server error');
    },
  });
}
function increment() {

  document.getElementById('bl_tubes').stepUp();
}
function decrement() {
  if (document.getElementById('bl_tubes').value == 0) {
    document.getElementById('bl_tubes').value = 0;
    return;
  }
  document.getElementById('bl_tubes').stepDown();
}