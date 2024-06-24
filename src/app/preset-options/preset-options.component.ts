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

  populatePresets(){ // triggered when presets dropdown is opened for the first time in current session
    let token = sessionStorage.getItem('user') 
    if(!token){
      alert('Please log in to view presets')
      return
    }
    if(this.presetsLoaded){ // prevents requests from being sent if the presets are already stored
      return
    }
    this.apiService.getPresets(token).subscribe( // sends get reguest to flask API's presets endpoint
      res => {
        console.log(res)
        this.presetOptions = res // stores response 
        this.presetsLoaded = true // track that the presets are already stored so that requests are not sent every time the user opens the dropdown
      }, 
      error => {
        console.log(error)
      }
    )
  }

  handleDropdown(e: any) { // triggered when a saved preset is clicked 
    if(e.value){
      // emit the selection as an array -- value is currently handled in the 'proposal-form' component
      this.presetSelected.emit(e.value.split(','))
    }
  }

  refreshPresets(){ // triggered when a new preset is saved (currently called in 'proposal-form' component)
    this.presetsLoaded = false 
    this.populatePresets() // calls the method that sends the get request to refresh the preset options with the new preset
  }

}
