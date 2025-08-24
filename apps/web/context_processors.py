def app_info(request):
    """Context processor to add app information to templates"""
    return {
        'app_name': 'DocuApp',
        'app_version': '1.0.0',
    }
