def uploadImg():
    from azure.storage.blob import BlockBlobService
    block_blob_service = BlockBlobService(account_name='eventdetect', account_key='VdqUAaFmd5K8bF5Pp+wt6cDfYUWiAtR2ib7+rKP76sqgJwSo0+friYmuVd+Y5oEWDh6/4oaRa423fXproar3aw==')
    block_blob_service.create_container('mycontainer')
    from azure.storage.blob import PublicAccess
    block_blob_service.create_container('mycontainer', public_access=PublicAccess.Container)
    block_blob_service.set_container_acl('mycontainer', public_access=PublicAccess.Container)
    from azure.storage.blob import ContentSettings
    block_blob_service.create_blob_from_path(
        'mycontainer',
        'myblockblob',
        'Images\\frame.jpg',
        content_settings=ContentSettings(content_type='image/jpg')
            )
