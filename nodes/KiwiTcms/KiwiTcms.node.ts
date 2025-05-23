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

    /**
     * Safely parses JSON while preserving all formatting
     * @param jsonString Input JSON string
     * @returns Parsed JSON object
     * @throws Error with detailed diagnostics if parsing fails
     */
    const safeJsonParse = (jsonString: string): any => {
        // First attempt - try parsing directly
        try {
            return JSON.parse(jsonString);
        } catch (initialError) {
            // Second attempt - minimal cleaning if first fails
            try {
                // Only remove truly invalid control characters (excluding \t, \n, \r)
                const cleaned = jsonString.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F]/g, '');
                return JSON.parse(cleaned);
            } catch (finalError) {
                // Generate detailed error report
                const err = finalError as Error;
                const positionMatch = err.message.match(/position (\d+)/);
                const position = positionMatch ? parseInt(positionMatch[1]) : 0;
                
                // Get character information
                const badChar = jsonString.charCodeAt(position);
                const contextStart = Math.max(0, position - 30);
                const contextEnd = Math.min(jsonString.length, position + 30);
                const context = jsonString.slice(contextStart, contextEnd);

                // Prepare error details
                const errorDetails = {
                    message: err.message,
                    position,
                    character: {
                        code: badChar,
                        hex: `U+${badChar.toString(16).padStart(4, '0')}`,
                        representation: badChar >= 32 ? String.fromCharCode(badChar) : '[control character]'
                    },
                    context,
                    inputSample: jsonString.length > 100 
                        ? `${jsonString.substring(0, 50)}...${jsonString.substring(jsonString.length - 50)}` 
                        : jsonString
                };

                throw new Error(
                    `JSON parsing failed after cleaning:\n` +
                    `• Error: ${errorDetails.message}\n` +
                    `• Position: ${errorDetails.position}\n` +
                    `• Character: ${errorDetails.character.representation} (${errorDetails.character.hex})\n` +
                    `• Context: "${errorDetails.context.replace(/\n/g, '\\n')}"\n` +
                    `• Input (abbreviated): "${errorDetails.inputSample.replace(/\n/g, '\\n')}"`
                );
            }
        }
    };

    for (let i = 0; i < items.length; i++) {
        try {
            // Get node parameters
            const credentials = await this.getCredentials('kiwiTcmsApi');
            const { url, username, password } = credentials;
            const action = this.getNodeParameter('action', i) as string;
            const rawParams = this.getNodeParameter('params', i) as string;

            // Validate and parse parameters
            let params: any = {};
            if (rawParams.trim()) {
                try {
                    params = safeJsonParse(rawParams);
                } catch (parseError) {
                    throw new NodeOperationError(
                        this.getNode(),
                        `Failed to parse input parameters:\n${(parseError as Error).message}`,
                        { itemIndex: i }
                    );
                }
            }

            // Prepare Python script input
            const inputData = {
                url,
                username,
                password,
                action,
                params
            };

            // Execute Python script with error handling
            let result: any;
            try {
                result = await new Promise<any>((resolve, reject) => {
                    const scriptPath = path.join(__dirname, 'tcms_script.py');
                    const py = spawn('/usr/bin/python3', [scriptPath]);
                    
                    let output = '';
                    let errorOutput = '';

                    py.stdin.write(JSON.stringify(inputData));
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
                            resolve(output ? JSON.parse(output) : {});
                        } catch (parseError) {
                            reject(new Error(`Failed to parse script output: ${(parseError as Error).message}`));
                        }
                    });
                });
            } catch (executionError) {
                throw new NodeOperationError(
                    this.getNode(),
                    `TCMS script execution failed:\n${(executionError as Error).message}`,
                    { itemIndex: i }
                );
            }

            // Format results
            if (Array.isArray(result)) {
                results.push(...result.map(item => ({ json: item })));
            } else if (result !== null && typeof result === 'object') {
                results.push({ json: result });
            } else {
                throw new NodeOperationError(
                    this.getNode(),
                    `Unexpected result format from TCMS script: ${typeof result}`,
                    { itemIndex: i }
                );
            }

        } catch (error) {
            if (error instanceof Error) {
                throw new NodeOperationError(this.getNode(), error.message, { itemIndex: i });
            }
            throw new NodeOperationError(this.getNode(), 'Unknown processing error', { itemIndex: i });
        }
    }

    return [results];
}
}
