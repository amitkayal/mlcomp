import {NgModule} from '@angular/core';
import {DagDetailModule} from './dag-detail/dag-detail.module';
import { DagComponent } from './dag/dag.component';
import {DagRoutingModule} from './dag-routing.module'
import {SharedModule} from "../shared.module";
import {DagRestartDialogComponent} from "./dags/dag-restart-dialog";

@NgModule({
    imports: [
        DagRoutingModule,
        DagDetailModule,
        SharedModule
    ],
    declarations: [
        DagComponent,
        DagRestartDialogComponent
    ],
    entryComponents:[
        DagRestartDialogComponent
    ]
})
export class DagModule {
}