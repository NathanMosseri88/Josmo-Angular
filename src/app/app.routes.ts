import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { ProposalFormComponent } from './proposal-form/proposal-form.component';

export const routes: Routes = [
    {path: 'login', component: LoginComponent},
    {path: 'proposal-form', component: ProposalFormComponent},
    {path: '', component: HomeComponent},
    {path: '**', component: NotFoundComponent}
];
