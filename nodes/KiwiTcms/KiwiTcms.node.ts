import {
    IExecuteFunctions,
    INodeExecutionData,
    INodeType,
    INodeTypeDescription,
    NodeOperationError,
} from 'n8n-workflow';
import * as path from 'path';
import { spawn } from 'node:child_process';

export class KiwiTcms implements INodeType {
    description: INodeTypeDescription = {
        displayName: 'Kiwi TCMS',
        name: 'kiwiTcms',
        icon: 'file:kiwi.svg',
        group: ['transform'],
        version: 1,
        description: 'Interact with Kiwi TCMS using Python tcms-api',
        defaults: {
            name: 'Kiwi TCMS',
        },
        inputs: ['main'],
        outputs: ['main'],
        credentials: [
            {
                name: 'kiwiTcmsApi',
                required: true,
            },
        ],
        properties: [
            {
                displayName: 'Action',
                name: 'action',
                type: 'options',
                options: [
                    { name: 'Build.create', value: 'Build.create' },
                    { name: 'Build.filter', value: 'Build.filter' },
                    { name: 'Build.update', value: 'Build.update' },
                    { name: 'Component.create', value: 'Component.create' },
                    { name: 'Component.filter', value: 'Component.filter' },
                    { name: 'Component.update', value: 'Component.update' },
                    { name: 'Environment.add_property', value: 'Environment.add_property' },
                    { name: 'Environment.create', value: 'Environment.create' },
                    { name: 'Environment.filter', value: 'Environment.filter' },
                    { name: 'Environment.properties', value: 'Environment.properties' },
                    { name: 'Environment.remove_property', value: 'Environment.remove_property' },
                    { name: 'Product.create', value: 'Product.create' },
                    { name: 'Product.filter', value: 'Product.filter' },
                    { name: 'Tag.filter', value: 'Tag.filter' },
                    { name: 'TestCase.add_attachment', value: 'TestCase.add_attachment' },
                    { name: 'TestCase.add_comment', value: 'TestCase.add_comment' },
                    { name: 'TestCase.add_component', value: 'TestCase.add_component' },
                    { name: 'TestCase.add_notification_cc', value: 'TestCase.add_notification_cc' },
                    { name: 'TestCase.add_property', value: 'TestCase.add_property' },
                    { name: 'TestCase.add_tag', value: 'TestCase.add_tag' },
                    { name: 'TestCase.comments', value: 'TestCase.comments' },
                    { name: 'TestCase.create', value: 'TestCase.create' },
                    { name: 'TestCase.filter', value: 'TestCase.filter' },
                    { name: 'TestCase.get_notification_cc', value: 'TestCase.get_notification_cc' },
                    { name: 'TestCase.history', value: 'TestCase.history' },
                    { name: 'TestCase.list_attachments', value: 'TestCase.list_attachments' },
                    { name: 'TestCase.properties', value: 'TestCase.properties' },
                    { name: 'TestCase.remove', value: 'TestCase.remove' },
                    { name: 'TestCase.remove_comment', value: 'TestCase.remove_comment' },
                    { name: 'TestCase.remove_component', value: 'TestCase.remove_component' },
                    { name: 'TestCase.remove_notification_cc', value: 'TestCase.remove_notification_cc' },
                    { name: 'TestCase.remove_property', value: 'TestCase.remove_property' },
                    { name: 'TestCase.remove_tag', value: 'TestCase.remove_tag' },
                    { name: 'TestCase.sortkeys', value: 'TestCase.sortkeys' },
                    { name: 'TestCase.update', value: 'TestCase.update' },
                    { name: 'TestExecution.add_comment', value: 'TestExecution.add_comment' },
                    { name: 'TestExecution.add_link', value: 'TestExecution.add_link' },
                    { name: 'TestExecution.filter', value: 'TestExecution.filter' },
                    { name: 'TestExecution.get_comments', value: 'TestExecution.get_comments' },
                    { name: 'TestExecution.get_links', value: 'TestExecution.get_links' },
                    { name: 'TestExecution.history', value: 'TestExecution.history' },
                    { name: 'TestExecution.properties', value: 'TestExecution.properties' },
                    { name: 'TestExecution.remove', value: 'TestExecution.remove' },
                    { name: 'TestExecution.remove_comment', value: 'TestExecution.remove_comment' },
                    { name: 'TestExecution.remove_link', value: 'TestExecution.remove_link' },
                    { name: 'TestExecution.update', value: 'TestExecution.update' },
                    { name: 'TestPlan.add_attachment', value: 'TestPlan.add_attachment' },
                    { name: 'TestPlan.add_case', value: 'TestPlan.add_case' },
                    { name: 'TestPlan.add_tag', value: 'TestPlan.add_tag' },
                    { name: 'TestPlan.create', value: 'TestPlan.create' },
                    { name: 'TestPlan.filter', value: 'TestPlan.filter' },
                    { name: 'TestPlan.list_attachments', value: 'TestPlan.list_attachments' },
                    { name: 'TestPlan.remove_case', value: 'TestPlan.remove_case' },
                    { name: 'TestPlan.remove_tag', value: 'TestPlan.remove_tag' },
                    { name: 'TestPlan.tree', value: 'TestPlan.tree' },
                    { name: 'TestPlan.update', value: 'TestPlan.update' },
                    { name: 'TestPlan.update_case_order', value: 'TestPlan.update_case_order' },
                    { name: 'TestRun.add_attachment', value: 'TestRun.add_attachment' },
                    { name: 'TestRun.add_case', value: 'TestRun.add_case' },
                    { name: 'TestRun.add_cc', value: 'TestRun.add_cc' },
                    { name: 'TestRun.add_tag', value: 'TestRun.add_tag' },
                    { name: 'TestRun.annotate_executions_with_properties', value: 'TestRun.annotate_executions_with_properties' },
                    { name: 'TestRun.create', value: 'TestRun.create' },
                    { name: 'TestRun.filter', value: 'TestRun.filter' },
                    { name: 'TestRun.get_cases', value: 'TestRun.get_cases' },
                    { name: 'TestRun.properties', value: 'TestRun.properties' },
                    { name: 'TestRun.remove', value: 'TestRun.remove' },
                    { name: 'TestRun.remove_case', value: 'TestRun.remove_case' },
                    { name: 'TestRun.remove_cc', value: 'TestRun.remove_cc' },
                    { name: 'TestRun.remove_tag', value: 'TestRun.remove_tag' },
                    { name: 'TestRun.update', value: 'TestRun.update' }
                ],
                default: 'TestCase.filter',
            },
            {
                displayName: 'Parameters',
                name: 'params',
                type: 'json',
                default: '{}',
                description: 'JSON object with parameters for the selected action',
            },
        ],
    };

   async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    const items = this.getInputData();
    const results: INodeExecutionData[] = [];

    for (let i = 0; i < items.length; i++) {
        try {
            const credentials = await this.getCredentials('kiwiTcmsApi');
            const url = credentials.url;
            const username = credentials.username;
            const password = credentials.password;
            const action = this.getNodeParameter('action', i) as string;

            
            let params = {};
            const rawParams = this.getNodeParameter('params', i) as string;
            
            if (rawParams.trim()) {
                try {
                    
                    const cleanedParams = rawParams
                        
                        .replace(/[\x00-\x08\x0B\x0C\x0E-\x1F]/g, '')
                        
                        .replace(/\\n/g, '\n')  
                        .replace(/\\r/g, '\r')  
                        .replace(/\\t/g, '\t'); 

                    params = JSON.parse(cleanedParams);
                } catch (error) {
                    
                    const errorPosition = parseInt(error.message.match(/position (\d+)/)?.[1] || '0');
                    const contextStart = Math.max(0, errorPosition - 50);
                    const contextEnd = Math.min(rawParams.length, errorPosition + 50);
                    const errorContext = rawParams.substring(contextStart, contextEnd);

                    throw new NodeOperationError(
                        this.getNode(), 
                        `Failed to parse JSON parameters: ${error.message}\n` +
                        `Problem area: ...${errorContext}...`
                    );
                }
            }

            
            const inputData = {
                url,
                username,
                password,
                action,
                params
            };

            const input = JSON.stringify(inputData);

            
            const result = await new Promise<any>((resolve, reject) => {
                const scriptPath = path.join(__dirname, 'tcms_script.py');
                const py = spawn('/usr/bin/python3', [scriptPath]);

                let output = '';
                let errorOutput = '';

                py.stdin.write(input);
                py.stdin.end();

                py.stdout.on('data', (data: Buffer) => {
                    output += data.toString();
                });

                py.stderr.on('data', (data: Buffer) => {
                    errorOutput += data.toString();
                });

                py.on('close', (code: number) => {
                    if (code !== 0) {
                        return reject(new Error(`Python script exited with code ${code}: ${errorOutput}`));
                    }

                    try {
                        const parsedOutput = output ? JSON.parse(output) : {};
                        resolve(parsedOutput);
                    } catch (error) {
                        reject(new Error(`Failed to parse Python script output: ${error.message}\nOutput: ${output.substring(0, 300)}...`));
                    }
                });
            });

            
            if (Array.isArray(result)) {
                results.push(...result.map(item => ({ json: item })));
            } else {
                results.push({ json: result });
            }

        } catch (error) {
            if (error instanceof Error) {
                throw new NodeOperationError(this.getNode(), error);
            }
            throw new NodeOperationError(this.getNode(), 'Unknown error occurred');
        }
    }

    return [results];
}
}