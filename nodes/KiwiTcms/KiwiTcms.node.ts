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
                displayName: 'Record ID (pk)',
                name: 'pk',
                type: 'number',
                required: true,
                displayOptions: {
                    show: {
                        action: ['TestCase.filter']
                    }
                },
                default: 0,
                description: 'ID case',
            },
            {
                displayName: 'Summary',
                name: 'summary',
                type: 'string',
                required: true,
                displayOptions: {
                    show: {
                        action: ['TestCase.create']
                    }
                },
                default: '',
                description: 'Brief description of the test case',
            },
            {
                displayName: 'Case Status ID',
                name: 'case_status',
                type: 'number',
                required: true,
                displayOptions: {
                    show: {
                        action: ['TestCase.create']
                    }
                },
                default: 2,
                description: 'Test case status',
            },
            {
                displayName: 'Category ID',
                name: 'category',
                type: 'number',
                required: true,
                displayOptions: {
                    show: {
                        action: ['TestCase.create']
                    }
                },
                default: 4,
                description: 'ID Category',
            },
            {
                displayName: 'Priority ID',
                name: 'priority',
                type: 'number',
                required: true,
                displayOptions: {
                    show: {
                        action: ['TestCase.create']
                    }
                },
                default: 1,
                description: 'Test case priority',
            },
            {
                displayName: 'Author ID',
                name: 'author',
                type: 'number',
                required: true,
                displayOptions: {
                    show: {
                        action: ['TestCase.create']
                    }
                },
                default: 25,
                description: 'Test case author ID ',
            },
            {
                displayName: 'Test Steps',
                name: 'text',
                type: 'string',
                typeOptions: {
                    rows: 4,
                },
                displayOptions: {
                    show: {
                        action: ['TestCase.create']
                    }
                },
                default: '',
                description: 'Test case steps (support Markdown)',
            },

            {
    displayName: 'Product ID',
    name: 'product',
    type: 'number',
    required: true,
    displayOptions: {
        show: {
            action: ['TestPlan.create']
        }
    },
    default: 3,
    description: 'Product ID',
},
{
    displayName: 'Product Version',
    name: 'product_version',
    type: 'number',
    required: true,
    displayOptions: {
        show: {
            action: ['TestPlan.create']
        }
    },
    default: 3,
    description: 'Product version',
},
{
    displayName: 'Product Name',
    name: 'product__name',
    type: 'string',
    required: true,
    displayOptions: {
        show: {
            action: ['TestPlan.create']
        }
    },
    default: 'FastReport .NET',
    description: 'Product display name',
},
{
    displayName: 'Plan Name',
    name: 'name',
    type: 'string',
    required: true,
    displayOptions: {
        show: {
            action: ['TestPlan.create']
        }
    },
    default: '',
    description: 'Name of test plan',
},
{
    displayName: 'Plan Type ID',
    name: 'type',
    type: 'number',
    required: true,
    displayOptions: {
        show: {
            action: ['TestPlan.create']
        }
    },
    default: 5,
    description: 'Type test plan (5 = Acceptance)',
},
{
    displayName: 'Plan Type Name',
    name: 'type__name',
    type: 'string',
    required: true,
    displayOptions: {
        show: {
            action: ['TestPlan.create']
        }
    },
    default: 'Acceptance (Приемочное)',
    description: 'Type display name',
},
{
    displayName: 'Description',
    name: 'text',
    type: 'string',
    typeOptions: {
        rows: 4,
    },
    displayOptions: {
        show: {
            action: ['TestPlan.create']
        }
    },
    default: '',
    description: 'Description test plan',
},
{
    displayName: 'Extra Link',
    name: 'extra_link',
    type: 'string',
    displayOptions: {
        show: {
            action: ['TestPlan.create']
        }
    },
    default: '',
    description: 'Extra link test plan',
},
{
    displayName: 'Is Active',
    name: 'is_active',
    type: 'boolean',
    displayOptions: {
        show: {
            action: ['TestPlan.create']
        }
    },
    default: true,
    description: 'Is active',
},

{
    displayName: 'Test Plan ID',
    name: 'plan_id',
    type: 'number',
    required: true,
    displayOptions: {
        show: {
            action: ['TestPlan.add_case']
        }
    },
    default: 0,
    description: 'ID of test plan to add case to',
},
{
    displayName: 'Test Case ID',
    name: 'case_id',
    type: 'number',
    required: true,
    displayOptions: {
        show: {
            action: ['TestPlan.add_case']
        }
    },
    default: 0,
    description: 'ID of test case to add',
}

            {
                displayName: 'Parameters',
                name: 'params',
                type: 'json',
                default: '{}',
                description: 'JSON object with parameters for the selected action',
                displayOptions: {
                    hide: {
                        action: ['TestCase.filter', 'TestCase.create','TestPlan.create']
                    }
                }
            },
        ],
    };

async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    const items = this.getInputData();
    const results: INodeExecutionData[] = [];

    /**
     * Specialized JSON parser for Kiwi TCMS that:
     * - Explicitly allows newlines in content
     * - Preserves Markdown formatting
     * - Handles multilingual text
     */
    const kiwiJsonParse = (jsonString: string): any => {
        // Pre-process to protect newlines in content areas
        const protectedString = jsonString
            // Protect newlines in string values
            .replace(/"([^"\\]*(?:\\.[^"\\]*)*)"/g, (match) => 
                match.replace(/\n/g, '\\n'))
            // Remove truly invalid characters
            .replace(/[\x00-\x08\x0B\x0C\x0E-\x1F]/g, '');

        try {
            // Parse and then restore newlines
            const parsed = JSON.parse(protectedString);
            const restoreNewlines = (obj: any): any => {
                if (typeof obj === 'string') {
                    return obj.replace(/\\n/g, '\n');
                }
                if (Array.isArray(obj)) {
                    return obj.map(restoreNewlines);
                }
                if (typeof obj === 'object' && obj !== null) {
                    return Object.fromEntries(
                        Object.entries(obj).map(([k, v]) => [k, restoreNewlines(v)])
                    );
                }
                return obj;
            };
            return restoreNewlines(parsed);
        } catch (error) {
            // Enhanced error diagnostics
            const err = error as Error;
            const positionMatch = err.message.match(/position (\d+)/);
            const position = positionMatch ? parseInt(positionMatch[1]) : 0;
            
            // Get context with 20 chars before/after
            const context = jsonString.substring(
                Math.max(0, position - 20),
                Math.min(jsonString.length, position + 20)
            );

            // Create annotated hex dump
            const hexDump = Array.from(context)
                .map((c, i) => {
                    const code = c.charCodeAt(0);
                    return `${i === 20 ? '>>>' : ''}${code.toString(16).padStart(4, '0')}${i === 20 ? '<<<' : ''}`;
                })
                .join(' ');

            throw new Error(
                `JSON PARSE ERROR:\n` +
                `• Message: ${err.message}\n` +
                `• Location: Char ${position}\n` +
                `• Context: "${context.replace(/\n/g, '\\n')}"\n` +
                `• Hex codes: ${hexDump}\n` +
                `• Document start: ${jsonString.substring(0, 100).replace(/\n/g, '\\n')}...`
            );
        }
    };

        for (let i = 0; i < items.length; i++) {
            try {
                const credentials = await this.getCredentials('kiwiTcmsApi');
                const { url, username, password } = credentials;
                const action = this.getNodeParameter('action', i) as string;
                
                let params = {};

                // Processing TestCase.filter
                if (action === 'TestCase.filter') {
                    const pk = this.getNodeParameter('pk', i) as number;
                    const rawParams = this.getNodeParameter('params', i, '{}') as string;
                    params = { pk };
                    if (rawParams.trim()) {
                        params = { ...params, ...kiwiJsonParse(rawParams) };
                    }
                }
                // Processing TestCase.create
                else if (action === 'TestCase.create') {
                    params = {
                        summary: this.getNodeParameter('summary', i) as string,
                        case_status: this.getNodeParameter('case_status', i) as number,
                        category: this.getNodeParameter('category', i) as number,
                        priority: this.getNodeParameter('priority', i) as number,
                        author: this.getNodeParameter('author', i) as number,
                        text: this.getNodeParameter('text', i) as string,
                    };
                    
                }
                // Processing TestPlan.create
                else if (action === 'TestPlan.create') {
                    params = {
                    product: this.getNodeParameter('product', i) as number,
                    product_version: this.getNodeParameter('product_version', i) as number,
                    product__name: this.getNodeParameter('product__name', i) as string,
                    name: this.getNodeParameter('name', i) as string,
                    type: this.getNodeParameter('type', i) as number,
                    type__name: this.getNodeParameter('type__name', i) as string,
                    text: this.getNodeParameter('text', i, '') as string,
                    extra_link: this.getNodeParameter('extra_link', i, '') as string,
                    is_active: this.getNodeParameter('is_active', i, true) as boolean,
                    parent: null
                    };
                }
                // Processing TestPlan.add_case
                else if (action === 'TestPlan.add_case') {
                    params = {
                    plan_id: this.getNodeParameter('plan_id', i) as number,
                    case_id: this.getNodeParameter('case_id', i) as number
                    };
                }
                // Processing of other methods
                else {
                    const rawParams = this.getNodeParameter('params', i) as string;
                    if (rawParams.trim()) {
                        params = kiwiJsonParse(rawParams);
                    }
                }

                // Execute Python script
                const result = await new Promise<any>((resolve, reject) => {
                    const scriptPath = path.join(__dirname, 'tcms_script.py');
                    const py = spawn('/usr/bin/python3', [scriptPath]);
                    
                    let output = '';
                    let errorOutput = '';

                    py.stdin.write(JSON.stringify({
                        url,
                        username,
                        password,
                        action,
                        params
                    }));
                    py.stdin.end();

                    py.stdout.on('data', (data: Buffer) => {
                        output += data.toString();
                    });

                    py.stderr.on('data', (data: Buffer) => {
                        errorOutput += data.toString();
                    });

                    py.on('close', (code: number) => {
                        if (code !== 0) {
                            return reject(new Error(`Python error ${code}: ${errorOutput}`));
                        }
                        try {
                            resolve(output ? JSON.parse(output) : {});
                        } catch (error) {
                            reject(new Error(`Output parse failed: ${(error as Error).message}`));
                        }
                    });
                });

                // Format results
                if (Array.isArray(result)) {
                    results.push(...result.map(item => ({ json: item })));
                } else {
                    results.push({ json: result });
                }

            } catch (error) {
                throw new NodeOperationError(
                    this.getNode(),
                    `Processing failed for item ${i}:\n${(error as Error).message}`,
                    { itemIndex: i }
                );
            }
        }

        return [results];
    }
}
