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
import { StyleSelectionComponent } from '../style-selection/style-selection.component';

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
    StyleSelectionComponent,
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

  constructor(private formBuilder: FormBuilder) {
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
    this.formData.value.styles = this.formData.value.styles.trim().split('\n')
    console.log(this.formData.value)
    // let cleanedRows = this.rows.filter((row) => {
    //   return row !== ''
    // })
    // this.formData.value.styles = cleanedRows
    // console.log(this.rows)
  }

  handleCancel(){
    this.formData.reset()
  }

  handleStylesInput(style:string){
    this.stylesForPreset.styles = style.trim().split('\n')
    // this.formData.value.styles = value.trim().split('\n')
  }
  handlePresetInput(name:string){
    this.stylesForPreset.name = name.trim()
  }

  handleSavePreset(){
    // console.log(this.formData.value.styles)
    console.log(this.stylesForPreset)
  }

  // rows: string[] = [''];

  // handlePaste(event: ClipboardEvent): void {
  //   if (!event.clipboardData){
  //     return;
  //   }
  //   const clipboardData = event.clipboardData;
  //   const pastedText = clipboardData.getData('text');
  //   const pastedRows = pastedText.split('\n');

  //   // this.rows = pastedRows.map(row => row.trim());
  //   pastedRows.forEach((row) => {
  //     this.rows.push(row.trim())
  //   })
  // }

  // addRow(): void {
  //   this.rows.push('');
  //   console.log(this.rows)
  // }
}
