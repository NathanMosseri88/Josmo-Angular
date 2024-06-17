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
  presetsLoaded= false

  @Output() presetSelected = new EventEmitter<string[]>()

  constructor(private apiService: ApiService){}

  populatePresets(){
    let token = sessionStorage.getItem('user')
    if(!token){
      alert('Please log in to view presets')
      return
    }
    if(this.presetsLoaded){
      return
    }
    this.apiService.getPresets(token).subscribe(
      res => {
        console.log(res)
        this.presetOptions = res
        this.presetsLoaded = true
      }, 
      error => {
        console.log(error)
      }
    )
  }

  handleDropdown(e: any) {
    if(e.value){
      this.presetSelected.emit(e.value.split(','))
    }
  }

  refreshPresets(){
    this.presetsLoaded = false
    this.populatePresets()
  }

}
