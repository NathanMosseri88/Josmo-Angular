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

  // hard coded options for form dropdowns -- should probably be changed later
  runTypes = ['Size Run', 'No Size Run']
  viewBy = ['UPC', 'Size']
  pairsCases = ['Pairs', 'Cases']
  includeColumns = ['Price', 'Cost', 'Landed', 'In Stock', 'ATS', 'Incoming', 'Brand', 'Descript', 'Note']
  stockFilters = ['In Stock Only', 'Include 0 Quantities']
  statuses = ['Active']

  stylesForPreset:any = {name: '', styles: []}

  formData: FormGroup

  rows: string[] = ['','','','','','','','','','','',]; // represent rows in the styles table form 

  // initializes the API services to send requests to the flask API
  // initializes Angular reactive forms form group to gather form data from inputs
  constructor(private formBuilder: FormBuilder, private apiService: ApiService) {
    this.formData = this.formBuilder.group({
      type: ['', Validators.nullValidator],
      view: ['', Validators.nullValidator],
      pairs_cases: ['', Validators.nullValidator],
      columns: [[], Validators.nullValidator],
      percent_profit: [null, Validators.nullValidator],
      price_limit: [null, Validators.nullValidator],
      filters: ['', Validators.nullValidator],
      status: ['', Validators.nullValidator],
      filename: ['', Validators.required],
      styles: [[], Validators.nullValidator],
      quantityLess: [null, Validators.nullValidator],
      quantityGreater: [null, Validators.nullValidator],
    });
  }

  handleSubmit(e:any){
    this.formData.value.styles = this.rows // sets the styles field in form data to the values of the rows of the styles table 

    let token = sessionStorage.getItem('user') // grab the users auth token from browser session storage
    if(!token){
      alert('Please log in to submit proposals')
      return
    }
    this.apiService.sendProposalForm(this.formData.value, token).subscribe( // post request to Flask API's proposals endpoint
      res => {
        console.log(res)
        this.formData.reset() // clears the form data
      },
      error => {
        console.log(error)
        alert(error.error.error) 
      }
    )
  }

  handleProposalClear(){ // clears formData -  not including styles 
    this.formData.reset()
    // this.rows = []
    // this.stylesForPreset.name = ''
  }
  handleStylesClear(){
    this.rows = []
    this.stylesForPreset.name = ''
  }

  handleStylesInput(style:string, index:number){ // allows rows of styles table to be edited/removed
    // if the changed row is edited with another value, that row is replaced at the index of the rows array,
    // if the changed row is now empty that row's index in the rows array is removed
    style !== '' ? this.rows[index] = style : this.rows.splice(index, 1)
  }

  handlePresetInput(name:string){ // stores the preset name for creating presets
    this.stylesForPreset.name = name.trim()
  }

  handleSavePreset(){ // send preset to flask API
    this.stylesForPreset.styles = this.rows // get rows from preset table 

    let token = sessionStorage.getItem('user') // get user's auth token from browser session storage
    if(!token){
      alert('Please log in to save presets')
      return
    }
    this.apiService.savePreset(this.stylesForPreset, token).subscribe( // send post request to flask API's presets endpoint
      res => {
        console.log(res)
        alert(`Styles preset "${this.stylesForPreset.name}" saved!`)
        this.presetOptionsComponent.refreshPresets() // when preset is created refresh the saved presets dropdown via get request to API's preset endpoint
      },
      error => {
        console.log(error.error.error)
        alert(error.error.error)
      }
    )
  }

 
  async handlePaste() { // triggered when 'paste' button is clicked
    try {
      // clears empty rows before pasting values
      this.rows = this.rows.filter((row) => {
        return row !== ''
      },[])
      const text = await navigator.clipboard.readText() // gets values from user's clipboard
      // splits clipboard data by new lines (excel rows copied from a column are seperated by new lines), cleans leading and trailing whitepsaces,
      // and adds the clipboard data to the rows array that represents the rows of the styles table
      text.split('\n').forEach(line => line !== '' ? this.rows.push(line.trim()) : null) 
    } catch (error){
      console.log(error)
    }
  }

  addRow(amount:number=1){ // triggered when 'add row' button is clicked
    // amount argument and loop to allow dynamic row creation if we/user want to add multiple rows at a time
    for(let i = 0; i < amount; i++){
      this.rows.push(''); // pushes empty string into rows array to add empty rows to table
    }
  }

  handlePresetSelection(selectedStyles: string[]){ // triggered when a saved preset is selected -- uses method in preset-options component
    this.rows.push(...selectedStyles) // adds styles from saved preset to rows array 
  }

  deleteRow(index:any){
    console.log(index)
    this.rows.splice(index, 1)
  }

  handlePercentProfit():boolean{
    if(this.formData.value.columns){
      return !!this.formData.value.columns.includes('Price')
    }
    return false
  }


}
