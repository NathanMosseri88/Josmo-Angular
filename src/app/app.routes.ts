import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { ProposalFormComponent } from './proposal-form/proposal-form.component';
import { SignupComponent } from './signup/signup.component';
import { StyleSelectionComponent } from './style-selection/style-selection.component';

export const routes: Routes = [
    {path: 'login', component: LoginComponent},
    {path: 'signup', component: SignupComponent},
    {path: 'proposal-form', component: ProposalFormComponent},
    {path: 'styles', component: StyleSelectionComponent},
    {path: '', component: HomeComponent},
    {path: '**', component: NotFoundComponent}
];
