import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Output } from '@angular/core';
import { MatFormField, MatLabel } from '@angular/material/form-field';
import { MatOption, MatSelect } from '@angular/material/select';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-preset-options',
  standalone: true,
  imports: [
    CommonModule,
    MatFormField,
    MatSelect,
    MatOption,
    MatLabel,
  ],
  templateUrl: './preset-options.component.html',
  styleUrl: './preset-options.component.css'
})
export class PresetOptionsComponent {
  presetOptions:any[] = []

  @Output() presetSelected = new EventEmitter<string[]>()

  constructor(private apiService: ApiService){}

  populatePresets(){
    this.apiService.getPresets().subscribe(
      res => {
        console.log(res)
        this.presetOptions = res
      }, 
      error => {
        console.log(error)
      }
    )
  }

  handleDropdown(e: any) {
    // console.log(e.value.split(','))
    this.presetSelected.emit(e.value.split(','))
    // console.log(this.presetSelected)
  }

}
