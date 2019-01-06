$(document).ready(function() {
	var table = $('#table_id').DataTable({
		data: {{dados}},
		"bFilter": true,
		"bInfo": true,
		"bPaginate": true,
		"bLengthChange": true,
		"bAutoWidth": true,
		"paging": true,
		"bSort": true,
		"bJQueryUI": true,
		"bRetrieve": true,
		"pageLength": 5,
		"aoColumns": [
			{ "mData": 'first_name' },
			{ "mData": 'last_name' },
			{ "mData": 'office_phone' },
			{ "mData": 'department' }
		]
	});

});
