import { Component } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { MatFormField, MatFormFieldControl } from '@angular/material/form-field';
import { MatSelect, MatOption } from '@angular/material/select';
import { MatLabel } from '@angular/material/form-field';
import { CommonModule } from '@angular/common';
import { MatInput } from '@angular/material/input';
import {MatCheckboxModule} from '@angular/material/checkbox'
import { MatCardModule } from '@angular/material/card';
import {MatButtonModule} from '@angular/material/button'
import { ApiService } from '../services/api.service';
import { MatTableModule } from '@angular/material/table';

@Component({
  selector: 'app-proposal-form',
  standalone: true,
  imports: [
    CommonModule,
    MatFormField,
    MatSelect,
    MatOption,
    MatLabel,
    MatInput,
    ReactiveFormsModule,
    MatCheckboxModule,
    MatCardModule,
    MatButtonModule,
    MatTableModule
  ],
  templateUrl: './proposal-form.component.html',
  styleUrl: './proposal-form.component.css'
})
export class ProposalFormComponent {
  runTypes = ['Size Run']
  viewBy = ['UPC', 'Size']
  pairsCases = ['Pairs', 'Cases']
  includeColumns = ['Price', 'Cost', 'Landed', 'In Stock', 'ATS', 'Incoming', 'Brand', 'Descript', 'Note']
  stockFilters = ['In Stock Only', 'Include 0 Quantities']
  statuses = ['Active']
  stylesForPreset:any = {name: '', styles: []}

  formData: FormGroup

  constructor(private formBuilder: FormBuilder, private apiService: ApiService) {
    this.formData = this.formBuilder.group({
      type: ['', Validators.nullValidator],
      view: ['', Validators.required],
      pC: ['', Validators.required],
      columns: [[], Validators.required],
      filters: ['', Validators.required],
      status: ['', Validators.required],
      filename: ['', Validators.required],
      styles: [[], Validators.required]
    });
  }
  handleStateChange(type: string, value: string){
    console.log(this.formData.value[type])
  }

  handleSubmit(e:any){
    // this.formData.value.styles.length > 0 || !this.formData.value.styles ? 
    // this.formData.value.styles = this.formData.value.styles.trim().split('\n') : 
    // alert('Styles input is required')
    this.rows.length > 0 ? this.formData.value.styles = this.rows : alert('Styles input is required')
    console.log(this.formData.value)
    this.apiService.sendProposalForm(this.formData.value).subscribe(
      res => {
        console.log(res)
        this.formData.reset()
      },
      error => {
        console.log(error)
        console.log(this.formData.value)
      }
    )
  }

  handleCancel(){
    this.formData.reset()
    this.rows = []
    this.stylesForPreset.name = ''
  }

  handleStylesInput(style:string, index:number){
    // this.stylesForPreset.styles = style.trim().split('\n')
    
    this.rows[index] = style
    console.log(style)
  }

  handlePresetInput(name:string){
    this.stylesForPreset.name = name.trim()
  }

  handleSavePreset(){
    this.stylesForPreset.styles = this.rows
    console.log(this.stylesForPreset)
    
    this.apiService.savePreset(this.stylesForPreset).subscribe(
      res => {
        console.log(res)
      },
      error => {
        console.log(error)
      }
    )
  }

  rows: string[] = [];

  async handlePaste() {
    try {
      const text = await navigator.clipboard.readText()
      text.split('\n').forEach(line => line !== '' ? this.rows.push(line.trim()) : null)
      console.log(text)
      console.log(this.rows)
    } catch (error){
      console.log(error)
    }
  }

  addRow(): void {
    this.rows.push('');
    console.log(this.rows)
  }
}
