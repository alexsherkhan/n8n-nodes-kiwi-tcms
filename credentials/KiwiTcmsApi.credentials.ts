import {
    ICredentialType,
    INodeProperties,
} from 'n8n-workflow';

export class KiwiTcmsApi implements ICredentialType {
    name = 'kiwiTcmsApi';
    displayName = 'KiwiTCMS API';
    documentationUrl = 'https://kiwitcms.readthedocs.io/en/latest/modules/tcms.rpc.api.html';
    properties: INodeProperties[] = [
        {
            displayName: 'Kiwi TCMS URL',
            name: 'url',
            type: 'string',
            default: '',
            required: true,
            placeholder: 'https://your-kiwi-instance.com/xml-rpc/',
        },
        {
            displayName: 'Username',
            name: 'username',
            type: 'string',
            default: '',
            required: true,
            placeholder:'username',
        },
        {
            displayName: 'Password',
            name: 'password',
            type: 'string',
            typeOptions: {
                password: true
            },
            default: '',
            required: true,
        },
    ];
}
