import { Component, ViewChild } from '@angular/core';
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
import { PresetOptionsComponent } from '../preset-options/preset-options.component';

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
    MatTableModule,
    PresetOptionsComponent
  ],
  templateUrl: './proposal-form.component.html',
  styleUrl: './proposal-form.component.css'
})
export class ProposalFormComponent {

  @ViewChild(PresetOptionsComponent) presetOptionsComponent!: PresetOptionsComponent

  runTypes = ['Size Run']
  viewBy = ['UPC', 'Size']
  pairsCases = ['Pairs', 'Cases']
  includeColumns = ['Price', 'Cost', 'Landed', 'In Stock', 'ATS', 'Incoming', 'Brand', 'Descript', 'Note']
  stockFilters = ['In Stock Only', 'Include 0 Quantities']
  statuses = ['Active']
  stylesForPreset:any = {name: '', styles: []}

  formData: FormGroup

  presetRows: string[] = []
  rows: string[] = [];

  constructor(private formBuilder: FormBuilder, private apiService: ApiService) {
    this.formData = this.formBuilder.group({
      type: ['', Validators.nullValidator],
      view: ['', Validators.required],
      pairs_cases: ['', Validators.required],
      columns: [[], Validators.required],
      filters: ['', Validators.required],
      status: ['', Validators.required],
      filename: ['', Validators.required],
      styles: [[], Validators.required],
      quantityLess: [null, Validators.nullValidator],
      quantityGreater: [null, Validators.nullValidator],
    });
  }

  handleSubmit(e:any){
    this.formData.value.styles = this.rows 

    let token = sessionStorage.getItem('user')
    if(!token){
      alert('Please log in to submit proposals')
      return
    }
    this.apiService.sendProposalForm(this.formData.value, token).subscribe(
      res => {
        console.log(res)
        this.formData.reset()
      },
      error => {
        console.log(error)
        alert(error.error.error)
      }
    )
  }

  handleCancel(){
    this.formData.reset()
    this.rows = []
    this.stylesForPreset.name = ''
  }

  handleStylesInput(style:string, index:number){    
    this.rows[index] = style
  }

  handlePresetInput(name:string){
    this.stylesForPreset.name = name.trim()
  }

  handleSavePreset(){
    this.stylesForPreset.styles = this.rows

    let token = sessionStorage.getItem('user')
    if(!token){
      alert('Please log in to save presets')
      return
    }
    this.apiService.savePreset(this.stylesForPreset, token).subscribe(
      res => {
        console.log(res)
        alert(`Styles preset "${this.stylesForPreset.name}" saved!`)
        this.presetOptionsComponent.refreshPresets()
      },
      error => {
        console.log(error.error.error)
        alert(error.error.error)
      }
    )
  }

 
  async handlePaste() {
    try {
      this.rows = this.rows.filter((row) => {
        return row !== ''
      },[])
      const text = await navigator.clipboard.readText()
      text.split('\n').forEach(line => line !== '' ? this.rows.push(line.trim()) : null)
    } catch (error){
      console.log(error)
    }
  }

  addRow(amount:number=1){
    for(let i = 0; i < amount; i++){
      this.rows.push('');
    }
  }

  handlePresetSelection(selectedStyles: string[]){
    this.rows.push(...selectedStyles)
  }


}
