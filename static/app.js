// DSynth - Frontend Application JavaScript

class DSynthApp {
    constructor() {
        this.currentSchema = null;
        this.currentCustomType = null;
        this.schemas = [];
        this.customTypes = [];
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadData();
        this.updateCounts();
    }

    bindEvents() {
        // Schema management
        document.getElementById('saveSchemaBtn').addEventListener('click', () => this.saveSchema());
        document.getElementById('addFieldBtn').addEventListener('click', () => this.showFieldModal());
        document.getElementById('loadSampleSchema').addEventListener('click', () => this.loadSampleSchema());
        
        // Custom type management
        document.getElementById('saveCustomTypeBtn').addEventListener('click', () => this.saveCustomType());
        document.getElementById('testCustomTypeBtn').addEventListener('click', () => this.testCustomType());
        
        // Field management
        document.getElementById('saveFieldBtn').addEventListener('click', () => this.saveField());
        document.getElementById('fieldName').addEventListener('change', (e) => this.onFieldNameChange(e));
        
        // Data generation
        document.getElementById('generateDataBtn').addEventListener('click', () => this.generateData());
        document.getElementById('copyDataBtn').addEventListener('click', () => this.copyData());
        document.getElementById('downloadDataBtn').addEventListener('click', () => this.downloadData());
        
        // Search functionality
        document.getElementById('schemaSearch').addEventListener('input', (e) => this.searchSchemas(e.target.value));
        document.getElementById('customTypeSearch').addEventListener('input', (e) => this.searchCustomTypes(e.target.value));
        
        // Modal events
        document.getElementById('schemaModal').addEventListener('show.bs.modal', (e) => this.onSchemaModalShow(e));
        document.getElementById('customTypeModal').addEventListener('show.bs.modal', (e) => this.onCustomTypeModalShow(e));
        document.getElementById('fieldModal').addEventListener('show.bs.modal', (e) => this.onFieldModalShow(e));
    }

    async loadData() {
        try {
            // Load schemas
            const schemasResponse = await fetch('/api/schemas');
            this.schemas = await schemasResponse.json();
            this.renderSchemas();
            
            // Load custom types
            const customTypesResponse = await fetch('/api/custom-types');
            this.customTypes = await customTypesResponse.json();
            this.renderCustomTypes();
            
            // Update schema select for data generation
            this.updateSchemaSelect();
            
        } catch (error) {
            console.error('Error loading data:', error);
            this.showAlert('Error loading data', 'danger');
        }
    }

    updateCounts() {
        document.getElementById('schema-count').textContent = this.schemas.length;
        document.getElementById('custom-type-count').textContent = this.customTypes.length;
        document.getElementById('data-count').textContent = '0';
    }

    // Schema Management
    renderSchemas() {
        const container = document.getElementById('schemasList');
        if (this.schemas.length === 0) {
            container.innerHTML = '<div class="text-center text-muted py-4"><i class="fas fa-inbox fa-3x mb-3"></i><p>No schemas found. Create your first schema to get started.</p></div>';
            return;
        }

        container.innerHTML = this.schemas.map(schema => `
            <div class="schema-card">
                <div class="schema-header">
                    <div>
                        <h5 class="schema-name">${schema.name}</h5>
                        <p class="schema-description">${schema.description || 'No description'}</p>
                    </div>
                    <div class="schema-actions">
                        <button class="btn btn-sm btn-outline-primary" onclick="app.editSchema('${schema.id}')">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="app.deleteSchema('${schema.id}')">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
                <div class="schema-meta">
                    <span><i class="fas fa-tag me-1"></i>${schema.schema_type.toUpperCase()}</span>
                    <span><i class="fas fa-database me-1"></i>${schema.seed_count} records</span>
                    <span><i class="fas fa-calendar me-1"></i>${new Date(schema.created_at).toLocaleDateString()}</span>
                    <span class="status-badge ${schema.is_active ? 'status-active' : 'status-inactive'}">
                        ${schema.is_active ? 'Active' : 'Inactive'}
                    </span>
                </div>
                <div class="mt-3">
                    <h6>Fields (${schema.fields.length})</h6>
                    ${schema.fields.map(field => `
                        <div class="field-item">
                            <div class="field-info">
                                <p class="field-name">${field.name}</p>
                                <p class="field-type">${field.data_type} ${field.required ? '(required)' : '(optional)'}</p>
                            </div>
                        </div>
                    `).join('')}
                </div>
                
                <!-- API Usage Help -->
                <div class="mt-3 api-help-section">
                    <button class="btn btn-outline-info btn-sm" type="button" data-bs-toggle="collapse" data-bs-target="#apiHelp-${schema.id}" aria-expanded="false">
                        <i class="fas fa-code me-1"></i>API Usage Examples
                    </button>
                    <div class="collapse mt-2" id="apiHelp-${schema.id}">
                        <div class="card card-body bg-light">
                            <h6 class="text-primary mb-2"><i class="fas fa-terminal me-1"></i>REST API Endpoints</h6>
                            
                            <div class="mb-3">
                                <h6 class="text-success">Generate Data</h6>
                                <div class="bg-dark text-light p-2 rounded mb-2">
                                    <code>POST /api/schemas/${schema.id}/generate</code>
                                </div>
                                <div class="row">
                                    <div class="col-md-6">
                                        <strong>Request Body:</strong>
                                        <pre class="bg-light p-2 rounded small">{
  "count": 10,
  "seed": 12345
}</pre>
                                    </div>
                                    <div class="col-md-6">
                                        <strong>cURL Example:</strong>
                                        <pre class="bg-light p-2 rounded small">curl -X POST "http://localhost:8000/api/schemas/${schema.id}/generate" \\
  -H "Content-Type: application/json" \\
  -d '{"count": 10, "seed": 12345}'</pre>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <h6 class="text-info">Get Schema Details</h6>
                                <div class="bg-dark text-light p-2 rounded mb-2">
                                    <code>GET /api/schemas/${schema.id}</code>
                                </div>
                                <div class="bg-light p-2 rounded small">
                                    <strong>cURL Example:</strong>
                                    <pre>curl "http://localhost:8000/api/schemas/${schema.id}"</pre>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <h6 class="text-warning">Get Schema Elements</h6>
                                <div class="bg-dark text-light p-2 rounded mb-2">
                                    <code>GET /api/schemas/${schema.id}/elements</code>
                                </div>
                                <div class="bg-light p-2 rounded small">
                                    <strong>cURL Example:</strong>
                                    <pre>curl "http://localhost:8000/api/schemas/${schema.id}/elements"</pre>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <h6 class="text-danger">Update Schema</h6>
                                <div class="bg-dark text-light p-2 rounded mb-2">
                                    <code>PUT /api/schemas/${schema.id}</code>
                                </div>
                                <div class="bg-light p-2 rounded small">
                                    <strong>cURL Example:</strong>
                                    <pre>curl -X PUT "http://localhost:8000/api/schemas/${schema.id}" \\
  -H "Content-Type: application/json" \\
  -d '{"name": "Updated Name", "schema_content": "..."}'</pre>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <h6 class="text-secondary">Delete Schema</h6>
                                <div class="bg-dark text-light p-2 rounded mb-2">
                                    <code>DELETE /api/schemas/${schema.id}</code>
                                </div>
                                <div class="bg-light p-2 rounded small">
                                    <strong>cURL Example:</strong>
                                    <pre>curl -X DELETE "http://localhost:8000/api/schemas/${schema.id}"</pre>
                                </div>
                            </div>
                            
                            <div class="alert alert-info mb-0">
                                <i class="fas fa-info-circle me-1"></i>
                                <strong>Base URL:</strong> <code>http://localhost:8000</code> (adjust for your deployment)
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    async saveSchema() {
        try {
            const formData = this.getSchemaFormData();
            if (!formData) return;

            const url = formData.id ? `/api/schemas/${formData.id}` : '/api/schemas';
            const method = formData.id ? 'PUT' : 'POST';

            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                this.showAlert('Schema saved successfully!', 'success');
                bootstrap.Modal.getInstance(document.getElementById('schemaModal')).hide();
                this.loadData();
            } else {
                const error = await response.json();
                this.showAlert(`Error saving schema: ${error.detail}`, 'danger');
            }
        } catch (error) {
            console.error('Error saving schema:', error);
            this.showAlert('Error saving schema', 'danger');
        }
    }

    getSchemaFormData() {
        const id = document.getElementById('schemaId').value;
        const name = document.getElementById('schemaName').value;
        const description = document.getElementById('schemaDescription').value;
        const schemaType = document.getElementById('schemaType').value;
        const schemaContent = document.getElementById('schemaContent').value;
        const seedCount = parseInt(document.getElementById('seedCount').value);

        if (!name || !schemaContent) {
            this.showAlert('Please fill in all required fields', 'danger');
            return null;
        }

        return {
            id: id || undefined,
            name,
            description,
            schema_type: schemaType,
            schema_content: schemaContent,
            seed_count: seedCount,
            fields: this.getSchemaFields()
        };
    }

    getSchemaFields() {
        const fields = [];
        const fieldElements = document.querySelectorAll('#schemaFields .field-item');
        
        fieldElements.forEach(element => {
            const name = element.querySelector('.field-name').textContent;
            const dataType = element.querySelector('.field-type').textContent.split(' ')[0];
            const required = element.querySelector('.field-type').textContent.includes('required');
            
            fields.push({
                name,
                data_type: dataType,
                required,
                nullable: !required
            });
        });
        
        return fields;
    }

    editSchema(schemaId) {
        const schema = this.schemas.find(s => s.id === schemaId);
        if (!schema) return;

        this.currentSchema = schema;
        document.getElementById('schemaModalTitle').textContent = 'Edit Schema';
        document.getElementById('schemaId').value = schema.id;
        document.getElementById('schemaName').value = schema.name;
        document.getElementById('schemaDescription').value = schema.description || '';
        document.getElementById('schemaType').value = schema.schema_type;
        document.getElementById('schemaContent').value = schema.schema_content;
        document.getElementById('seedCount').value = schema.seed_count;
        
        this.renderSchemaFields(schema.fields);
        
        const modal = new bootstrap.Modal(document.getElementById('schemaModal'));
        modal.show();
    }

    async deleteSchema(schemaId) {
        if (!confirm('Are you sure you want to delete this schema?')) return;

        try {
            const response = await fetch(`/api/schemas/${schemaId}`, { method: 'DELETE' });
            if (response.ok) {
                this.showAlert('Schema deleted successfully!', 'success');
                this.loadData();
            } else {
                this.showAlert('Error deleting schema', 'danger');
            }
        } catch (error) {
            console.error('Error deleting schema:', error);
            this.showAlert('Error deleting schema', 'danger');
        }
    }

    // Custom Type Management
    renderCustomTypes() {
        const container = document.getElementById('customTypesList');
        if (this.customTypes.length === 0) {
            container.innerHTML = '<div class="text-center text-muted py-4"><i class="fas fa-cogs fa-3x mb-3"></i><p>No custom types found. Create your first custom type to get started.</p></div>';
            return;
        }

        container.innerHTML = this.customTypes.map(type => `
            <div class="custom-type-card">
                <div class="custom-type-header">
                    <div>
                        <h5 class="custom-type-name">${type.name}</h5>
                        <p class="custom-type-description">${type.description || 'No description'}</p>
                    </div>
                    <div class="custom-type-actions">
                        <button class="btn btn-sm btn-outline-info" onclick="app.testCustomType('${type.id}')">
                            <i class="fas fa-play"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-primary" onclick="app.editCustomType('${type.id}')">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="app.deleteCustomType('${type.id}')">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
                <div class="custom-type-meta">
                    <span><i class="fas fa-code me-1"></i>MVEL Expression</span>
                    <span><i class="fas fa-calendar me-1"></i>${new Date(type.created_at).toLocaleDateString()}</span>
                    <span class="status-badge ${type.is_active ? 'status-active' : 'status-inactive'}">
                        ${type.is_active ? 'Active' : 'Inactive'}
                    </span>
                </div>
                <div class="mt-3">
                    <code class="bg-light p-2 rounded d-block">${type.mvel_expression}</code>
                    ${type.test_result ? `
                        <div class="test-result ${type.test_result.success ? 'test-success' : 'test-error'}">
                            <strong>Test Result:</strong> ${type.test_result.success ? 
                                `Sample: ${JSON.stringify(type.test_result.sample_data)}` : 
                                `Error: ${type.test_result.error}`}
                        </div>
                    ` : ''}
                </div>
            </div>
        `).join('');
    }

    async saveCustomType() {
        try {
            const formData = this.getCustomTypeFormData();
            if (!formData) return;

            const url = formData.id ? `/api/custom-types/${formData.id}` : '/api/custom-types';
            const method = formData.id ? 'PUT' : 'POST';

            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                this.showAlert('Custom type saved successfully!', 'success');
                bootstrap.Modal.getInstance(document.getElementById('customTypeModal')).hide();
                this.loadData();
            } else {
                const error = await response.json();
                this.showAlert(`Error saving custom type: ${error.detail}`, 'danger');
            }
        } catch (error) {
            console.error('Error saving custom type:', error);
            this.showAlert('Error saving custom type', 'danger');
        }
    }

    getCustomTypeFormData() {
        const id = document.getElementById('customTypeId').value;
        const name = document.getElementById('customTypeName').value;
        const description = document.getElementById('customTypeDescription').value;
        const mvelExpression = document.getElementById('mvelExpression').value;

        if (!name || !mvelExpression) {
            this.showAlert('Please fill in all required fields', 'danger');
            return null;
        }

        return {
            id: id || undefined,
            name,
            description,
            mvel_expression: mvelExpression
        };
    }

    editCustomType(typeId) {
        const customType = this.customTypes.find(t => t.id === typeId);
        if (!customType) return;

        this.currentCustomType = customType;
        document.getElementById('customTypeModalTitle').textContent = 'Edit Custom Type';
        document.getElementById('customTypeId').value = customType.id;
        document.getElementById('customTypeName').value = customType.name;
        document.getElementById('customTypeDescription').value = customType.description || '';
        document.getElementById('mvelExpression').value = customType.mvel_expression;
        
        const modal = new bootstrap.Modal(document.getElementById('customTypeModal'));
        modal.show();
    }

    async deleteCustomType(typeId) {
        if (!confirm('Are you sure you want to delete this custom type?')) return;

        try {
            const response = await fetch(`/api/custom-types/${typeId}`, { method: 'DELETE' });
            if (response.ok) {
                this.showAlert('Custom type deleted successfully!', 'success');
                this.loadData();
            } else {
                this.showAlert('Error deleting custom type', 'danger');
            }
        } catch (error) {
            console.error('Error deleting custom type:', error);
            this.showAlert('Error deleting custom type', 'danger');
        }
    }

    async testCustomType(typeId) {
        try {
            const response = await fetch(`/api/custom-types/${typeId}/test`, { method: 'POST' });
            const result = await response.json();
            
            if (result.success) {
                this.showAlert(`Test successful! Sample data: ${JSON.stringify(result.sample_data)}`, 'success');
            } else {
                this.showAlert(`Test failed: ${result.error}`, 'danger');
            }
        } catch (error) {
            console.error('Error testing custom type:', error);
            this.showAlert('Error testing custom type', 'danger');
        }
    }

    // Field Management
    async showFieldModal() {
        this.currentFieldIndex = null;
        this.clearFieldForm();
        
        // Load schema elements for the dropdown
        if (this.currentSchema && this.currentSchema.id) {
            await this.loadSchemaElements();
        }
        
        const modal = new bootstrap.Modal(document.getElementById('fieldModal'));
        modal.show();
    }

    async editField(index) {
        this.currentFieldIndex = index;
        const field = this.currentSchema.fields[index];
        
        // Load schema elements for the dropdown
        if (this.currentSchema && this.currentSchema.id) {
            await this.loadSchemaElements();
        }
        
        this.populateFieldForm(field);
        const modal = new bootstrap.Modal(document.getElementById('fieldModal'));
        modal.show();
    }

    async loadSchemaElements() {
        try {
            const response = await fetch(`/api/schemas/${this.currentSchema.id}/elements`);
            if (response.ok) {
                const data = await response.json();
                this.populateFieldNameDropdown(data.elements);
            } else {
                console.error('Error loading schema elements:', response.statusText);
            }
        } catch (error) {
            console.error('Error loading schema elements:', error);
        }
    }

    populateFieldNameDropdown(elements) {
        const dropdown = document.getElementById('fieldName');
        dropdown.innerHTML = '<option value="">Select a schema element...</option>';
        
        elements.forEach(element => {
            const option = document.createElement('option');
            option.value = element.name;
            option.textContent = `${element.name} (${element.type})`;
            option.dataset.elementType = element.type;
            option.dataset.required = element.required;
            option.dataset.description = element.description || '';
            dropdown.appendChild(option);
        });
    }

    onFieldNameChange(event) {
        const selectedOption = event.target.options[event.target.selectedIndex];
        if (selectedOption.value) {
            // Auto-populate data type and required fields based on schema element
            const dataTypeSelect = document.getElementById('fieldDataType');
            const requiredSelect = document.getElementById('fieldRequired');
            const descriptionField = document.getElementById('fieldDescription');
            
            // Set data type
            const elementType = selectedOption.dataset.elementType;
            if (elementType) {
                // Map schema types to our data types
                const typeMapping = {
                    'string': 'string',
                    'integer': 'integer',
                    'float': 'float',
                    'boolean': 'boolean',
                    'date': 'date',
                    'datetime': 'datetime',
                    'object': 'string'  // Default to string for complex types
                };
                const mappedType = typeMapping[elementType] || 'string';
                dataTypeSelect.value = mappedType;
            }
            
            // Set required field
            const isRequired = selectedOption.dataset.required === 'true';
            requiredSelect.value = isRequired.toString();
            
            // Set description
            const description = selectedOption.dataset.description;
            if (description) {
                descriptionField.value = description;
            }
        }
    }

    clearFieldForm() {
        document.getElementById('fieldName').innerHTML = '<option value="">Select a schema element...</option>';
        document.getElementById('fieldDataType').value = 'string';
        document.getElementById('fieldRequired').value = 'true';
        document.getElementById('fieldNullable').value = 'false';
        document.getElementById('fieldMvelExpression').value = '';
        document.getElementById('fieldDescription').value = '';
    }

    populateFieldForm(field) {
        // Set the field name dropdown value
        const fieldNameSelect = document.getElementById('fieldName');
        const option = Array.from(fieldNameSelect.options).find(opt => opt.value === field.name);
        if (option) {
            fieldNameSelect.value = field.name;
        }
        
        document.getElementById('fieldDataType').value = field.data_type;
        document.getElementById('fieldRequired').value = field.required.toString();
        document.getElementById('fieldNullable').value = field.nullable.toString();
        document.getElementById('fieldMvelExpression').value = field.mvel_expression || '';
        document.getElementById('fieldDescription').value = field.description || '';
    }

    saveField() {
        const fieldData = {
            name: document.getElementById('fieldName').value,
            data_type: document.getElementById('fieldDataType').value,
            required: document.getElementById('fieldRequired').value === 'true',
            nullable: document.getElementById('fieldNullable').value === 'true',
            mvel_expression: document.getElementById('fieldMvelExpression').value || null,
            description: document.getElementById('fieldDescription').value || null
        };

        if (!fieldData.name) {
            this.showAlert('Field name is required', 'danger');
            return;
        }

        if (this.currentFieldIndex !== null) {
            // Edit existing field
            this.currentSchema.fields[this.currentFieldIndex] = fieldData;
        } else {
            // Add new field
            this.currentSchema.fields.push(fieldData);
        }

        this.renderSchemaFields(this.currentSchema.fields);
        bootstrap.Modal.getInstance(document.getElementById('fieldModal')).hide();
    }

    renderSchemaFields(fields) {
        const container = document.getElementById('schemaFields');
        container.innerHTML = fields.map((field, index) => `
            <div class="field-item">
                <div class="field-info">
                    <p class="field-name">${field.name}</p>
                    <p class="field-type">${field.data_type} ${field.required ? '(required)' : '(optional)'}</p>
                </div>
                <div class="field-actions">
                    <button class="btn btn-sm btn-outline-primary" onclick="app.editField(${index})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="app.removeField(${index})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('');
    }

    removeField(index) {
        if (confirm('Are you sure you want to remove this field?')) {
            this.currentSchema.fields.splice(index, 1);
            this.renderSchemaFields(this.currentSchema.fields);
        }
    }

    // Data Generation
    async generateData() {
        const schemaId = document.getElementById('dataSchemaSelect').value;
        const count = parseInt(document.getElementById('dataCount').value);
        const seed = document.getElementById('dataSeed').value;

        if (!schemaId) {
            this.showAlert('Please select a schema', 'danger');
            return;
        }

        try {
            document.getElementById('generateDataBtn').disabled = true;
            document.getElementById('generateDataBtn').innerHTML = '<span class="loading"></span> Generating...';

            const response = await fetch(`/api/schemas/${schemaId}/generate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ count, seed: seed ? parseInt(seed) : null })
            });

            if (response.ok) {
                const result = await response.json();
                this.displayGeneratedData(result.data);
                document.getElementById('data-count').textContent = result.count;
            } else {
                const error = await response.json();
                this.showAlert(`Error generating data: ${error.detail}`, 'danger');
            }
        } catch (error) {
            console.error('Error generating data:', error);
            this.showAlert('Error generating data', 'danger');
        } finally {
            document.getElementById('generateDataBtn').disabled = false;
            document.getElementById('generateDataBtn').innerHTML = '<i class="fas fa-magic me-2"></i>Generate Data';
        }
    }

    displayGeneratedData(data) {
        const container = document.getElementById('generatedData');
        container.textContent = JSON.stringify(data, null, 2);
    }

    copyData() {
        const data = document.getElementById('generatedData').textContent;
        if (data && data !== 'No data generated yet. Select a schema and click "Generate Data".') {
            navigator.clipboard.writeText(data).then(() => {
                this.showAlert('Data copied to clipboard!', 'success');
            });
        }
    }

    downloadData() {
        const data = document.getElementById('generatedData').textContent;
        if (data && data !== 'No data generated yet. Select a schema and click "Generate Data".') {
            const blob = new Blob([data], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'generated_data.json';
            a.click();
            URL.revokeObjectURL(url);
        }
    }

    // Search functionality
    searchSchemas(query) {
        const filteredSchemas = this.schemas.filter(schema => 
            schema.name.toLowerCase().includes(query.toLowerCase()) ||
            (schema.description && schema.description.toLowerCase().includes(query.toLowerCase()))
        );
        this.renderFilteredSchemas(filteredSchemas);
    }

    searchCustomTypes(query) {
        const filteredTypes = this.customTypes.filter(type => 
            type.name.toLowerCase().includes(query.toLowerCase()) ||
            (type.description && type.description.toLowerCase().includes(query.toLowerCase()))
        );
        this.renderFilteredCustomTypes(filteredTypes);
    }

    renderFilteredSchemas(schemas) {
        const container = document.getElementById('schemasList');
        if (schemas.length === 0) {
            container.innerHTML = '<div class="text-center text-muted py-4"><i class="fas fa-search fa-3x mb-3"></i><p>No schemas found matching your search.</p></div>';
            return;
        }
        // Reuse the same rendering logic
        this.schemas = schemas;
        this.renderSchemas();
    }

    renderFilteredCustomTypes(types) {
        const container = document.getElementById('customTypesList');
        if (types.length === 0) {
            container.innerHTML = '<div class="text-center text-muted py-4"><i class="fas fa-search fa-3x mb-3"></i><p>No custom types found matching your search.</p></div>';
            return;
        }
        // Reuse the same rendering logic
        this.customTypes = types;
        this.renderCustomTypes();
    }

    // Utility methods
    showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    loadSampleSchema() {
        const schemaType = document.getElementById('schemaType').value;
        const sampleContent = this.getSampleSchema(schemaType);
        document.getElementById('schemaContent').value = sampleContent;
    }

    getSampleSchema(type) {
        if (type === 'json') {
            return JSON.stringify({
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "Unique identifier"},
                    "name": {"type": "string", "description": "Full name"},
                    "email": {"type": "string", "format": "email", "description": "Email address"},
                    "age": {"type": "integer", "minimum": 0, "maximum": 120, "description": "Age in years"},
                    "active": {"type": "boolean", "description": "Account status"}
                },
                "required": ["id", "name", "email"]
            }, null, 2);
        } else if (type === 'xml') {
            return `<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="person">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="id" type="xs:integer"/>
                <xs:element name="name" type="xs:string"/>
                <xs:element name="email" type="xs:string"/>
                <xs:element name="age" type="xs:integer" minOccurs="0"/>
                <xs:element name="active" type="xs:boolean" default="true"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
</xs:schema>`;
        }
        return '';
    }

    updateSchemaSelect() {
        const select = document.getElementById('dataSchemaSelect');
        select.innerHTML = '<option value="">Choose a schema...</option>';
        
        this.schemas.forEach(schema => {
            const option = document.createElement('option');
            option.value = schema.id;
            option.textContent = schema.name;
            select.appendChild(option);
        });
    }

    // Modal event handlers
    onSchemaModalShow(event) {
        if (!this.currentSchema) {
            // New schema
            document.getElementById('schemaModalTitle').textContent = 'New Schema';
            document.getElementById('schemaId').value = '';
            document.getElementById('schemaName').value = '';
            document.getElementById('schemaDescription').value = '';
            document.getElementById('schemaType').value = 'json';
            document.getElementById('schemaContent').value = '';
            document.getElementById('seedCount').value = '100';
            document.getElementById('schemaFields').innerHTML = '';
        }
    }

    onCustomTypeModalShow(event) {
        if (!this.currentCustomType) {
            // New custom type
            document.getElementById('customTypeModalTitle').textContent = 'New Custom Type';
            document.getElementById('customTypeId').value = '';
            document.getElementById('customTypeName').value = '';
            document.getElementById('customTypeDescription').value = '';
            document.getElementById('mvelExpression').value = '';
        }
    }

    onFieldModalShow(event) {
        // Field modal is handled by showFieldModal and editField methods
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new DSynthApp();
}); 