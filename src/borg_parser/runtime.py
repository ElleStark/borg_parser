# Borg runtime statistics

import pandas as pd
import numpy as np
from more_itertools import consecutive_groups
import matplotlib.pyplot as plt
import seaborn as sns
# import pygmo
import hiplot as hip
sns.set()


class BorgRuntimeUtils:
    """
    Borg multi-objective algorithm runtime parsing utilities
    """
    def _parse_stats(self, df_raw):
        """
        Convert Borg MOEA runtime file to pandas DataFrame
        Parameters
        ----------
        path : str
            Path to Borg MOEA runtime file
        decision_names : list
            Decision names
        objective_names : list
            Objective names
        Returns
        -------
        pandas.DataFrame
            Parsed runtime file
        """
        # Omit Population Prints
        df_res = df_raw[-np.isnan(df_raw['value'])]

        # Replace //
        df_res = pd.DataFrame(
            [df_res['var'].str.replace('//', ''), df_res['value']]
        ).T

        # Add index
        # JRK: our version of the runtime file only has 11
        # entries, not 13
        df_res['nfe_index'] = \
            [i for i in np.arange(0, len(df_res) // 11) for j in range(11)]

        # Parse Data Into Columns
        df_res = pd.pivot(
            df_res,
            columns='var',
            values='value',
            index='nfe_index'
        ).reset_index(drop=True)

        # Convert to Float
        df_res = df_res.astype(float)

        df_res.index = df_res['NFE'].astype(int)

        return df_res

    def _parse_archive(
        self,
        df,
        n_decisions,
        n_objectives,
        n_metrics
    ):
        """
        Convert archive data to dataframes
        Parameters
        ----------
        df : pandas.DataFrame
            Raw runtime pandas dataframe
        n_decisions : int
            Number of decisions
        n_objectives : int
            Number of objectives
        n_metrics : int
            Number of metrics
        Returns
        -------
        tuple
            Tuple of decisions, objectives, and metrics list of lists
        """
        # Extract Archive Prints
        df_temp = df[np.isnan(df['value'])]
        df_temp = df_temp[df_temp['var'] != '#']

        # Separate Based on Deliminators
        df_temp = df_temp['var'].str.split(' ', expand=True).astype(float)

        # Extract decisions, objectives, metrics from archive
        start_idx = 0
        end_idx = n_decisions
        df_all_decisions = df_temp.iloc[:, start_idx:end_idx]
        start_idx = end_idx
        end_idx = start_idx + n_objectives
        df_all_objectives = df_temp.iloc[:, start_idx:end_idx]
        start_idx = end_idx
        end_idx = start_idx + n_metrics
        df_all_metrics = df_temp.iloc[:, start_idx:end_idx]

        # Turn into list of lists
        decisions_ls = [
            df_all_decisions.loc[i].values.tolist()
            for i in consecutive_groups(df_all_decisions.index)
        ]
        objectives_ls = [
            df_all_objectives.loc[i].values.tolist()
            for i in consecutive_groups(df_all_objectives.index)
        ]
        metrics_ls = [
            df_all_metrics.loc[i].values.tolist()
            for i in consecutive_groups(df_all_metrics.index)
        ]

        return decisions_ls, objectives_ls, metrics_ls


class BorgRuntimeDiagnostic(BorgRuntimeUtils):
    """
    Borg multi-objective algorithm runtime diagnostics
    """
    def __init__(
        self,
        path_to_runtime,
        n_decisions,
        n_objectives,
        n_metrics,
    ):
        """
        Parsing runtime file and assigning parameters
        Parameters
        ----------
        path_to_runtime : str
            Path to Borg runtime file
        decision_names : list
            List of decision names
        objective_names : list
            List of objective names
        df_metrics : pandas.DataFrame
            Dataframe of decisions and corresponding metrics
        """
        super().__init__()

        # Read input file
        df_raw = pd.read_table(
            path_to_runtime,
            names=['var', 'value'],
            sep="="
        )

        # General attributes
        self.n_decisions = n_decisions
        self.n_objectives = n_objectives
        self.n_metrics = n_metrics

        # Defaults
        self.decision_names = [
            'decision_' + str(i+1) for i in range(n_decisions)
        ]
        self.objective_names = [
            'objective_' + str(i+1) for i in range(n_objectives)
        ]
        self.metric_names = [
            'metric_' + str(i+1) for i in range(n_metrics)
        ]

        # Runtime statistics
        df_res = self._parse_stats(
            df_raw
        )

        # JRK: removed entries that our version doesn't have
        self.nfe = df_res.index.to_list()
        self.archive_size = df_res['ArchiveSize'].to_dict()
        #self.elapsed_time = df_res['ElapsedTime'].to_dict()
        self.improvements = df_res['Improvements'].to_dict()
        #self.mutation_index = df_res['MutationIndex'].to_dict()
        self.population_size = df_res['PopulationSize'].to_dict()
        self.restarts = df_res['Restarts'].to_dict()
        self.pcx = df_res['PCX'].to_dict()
        self.de = df_res['DE'].to_dict()
        self.sbx = df_res['SBX'].to_dict()
        self.spx = df_res['SPX'].to_dict()
        self.um = df_res['UM'].to_dict()
        self.undx = df_res['UNDX'].to_dict()

        # Parsing archives
        decisions_ls, objectives_ls, metrics_ls = self._parse_archive(
            df_raw,
            self.n_decisions,
            self.n_objectives,
            self.n_metrics
        )
        self.archive_decisions = dict(zip(self.nfe, decisions_ls))
        self.archive_objectives = dict(zip(self.nfe, objectives_ls))
        self.archive_metrics = dict(zip(self.nfe, metrics_ls))

    def set_decision_names(self, decision_names):
        """Set decision names
        Parameters
        ----------
        decision_names : list
            Decision names
        """
        self.decision_names = decision_names

    def set_objective_names(self, objective_names):
        """Set decision names
        Parameters
        ----------
        objective_names : list
            Objective names
        """
        self.objective_names = objective_names

    def set_metric_names(self, metric_names):
        """Set metric names
        Parameters
        ----------
        metric_names : list
            Metric names
        """
        self.metric_names = metric_names

    # def compute_hypervolume(self, reference_point):
    #     """Compute hypervolumes
    #     Parameters
    #     ----------
    #     reference_point : list
    #         Reference point for hypervolume calculation. Length must be same
    #          as objectives
    #     """
    #     # Setup
    #     hypervolume_dict = {}

    #     for nfe, objs in self.archive_objectives.items():
    #         # Compute hypervolume
    #         hv = pygmo.hypervolume(objs)
    #         hv_val = hv.compute(ref_point=reference_point)

    #         # Store value
    #         hypervolume_dict[nfe] = hv_val

    #     self.hypervolume = hypervolume_dict

    def plot_improvements(
        self,
        y_lab='Improvements',
        x_lab='Function Evaluations'
    ):
        """
        Plot improvements over the search

        Parameters
        ----------
        y_lab : str
            Y label
        x_lab : str
            X label

        Returns
        -------
        matplotlib.figure.Figure
            Plot of improvements
        """
        # Get data
        df = pd.Series(self.improvements).to_frame().reset_index()

        # Plot
        fig = plt.figure()
        sns.lineplot(data=df, x='index', y=0)
        plt.ylabel(y_lab)
        plt.xlabel(x_lab)

        return fig

    def plot_constraint_violations(
        self,
        y_lab='value',
        x_lab='Function Evaluations'
    ):
        """
        Plot constraint violations over the search

        Parameters
        ----------
        y_lab : str
            Y label
        x_lab : str
            X label

        Returns
        -------
        matplotlib.figure.Figure
            Plot of constraint violations
        """
        # Get data
        df = pd.Series(self.improvements).to_frame().reset_index()

        # Plot
        fig = plt.figure()
        sns.lineplot(data=df, x='index', y=0)
        plt.ylabel(y_lab)
        plt.xlabel(x_lab)

        return fig

    # def plot_hypervolume(self, reference_point):
    #     """
    #     Plot hypervolume over the search
    #     Parameters
    #     ----------
    #     reference_point : list
    #         Reference point for hypervolume calculation
    #     Returns
    #     -------
    #     matplotlib.figure.Figure
    #         Plot of improvments
    #     """
    #     sns.set()

    #     # Computing hypervolume
    #     self.compute_hypervolume(reference_point)
    #     df_run = pd.DataFrame()
    #     df_run['hypervolume'] = pd.Series(self.hypervolume)
    #     df_run['nfe'] = df_run.index

    #     # Plotting
    #     fig, ax = plt.subplots()
    #     sns.lineplot(
    #         data=df_run,
    #         x='nfe',
    #         y='hypervolume',
    #         ax=ax
    #     )
    #     plt.ylabel('Hypervolume')
    #     plt.xlabel('Function Evaluations')

    #     return fig

    def plot_interactive_front(self):
        """
        Create interactive parallel plot
        Returns
        -------
        hiplot.experiment.Experiment
            Hiplot experiment
        """
        # Get final front
        nfe = self.nfe[-1]
        df_decs = pd.DataFrame(
            self.archive_decisions[nfe],
            columns=self.decision_names
        )
        df_objs = pd.DataFrame(
            self.archive_objectives[nfe],
            columns=self.objective_names
        )
        df_metrics = pd.DataFrame(
            self.archive_metrics[nfe],
            columns=self.metric_names
        )
        df_front = pd.concat([df_decs, df_objs, df_metrics], axis=1)

        # Create Plot
        cols = \
            self.decision_names +\
            self.objective_names +\
            self.metric_names
        cols.reverse()
        color_col = self.objective_names[0]
        exp = hip.Experiment.from_dataframe(df_front)
        exp.parameters_definition[color_col].colormap = 'interpolateViridis'
        exp.display_data(hip.Displays.PARALLEL_PLOT).update(
            {'order': cols}
        )
        exp.display_data(hip.Displays.TABLE).update(
            {'hide': ['uid', 'from_uid']}
        )

        return exp

    def plot_objectives_parcoord(self):
        """
        Create interactive parallel plot of objective values for archive solutions
        Returns
        -------
        hiplot.experiment.Experiment
            Hiplot experiment
        """
        # Get final front
        nfe = self.nfe[-1]
        """
        df_decs = pd.DataFrame(
            self.archive_decisions[nfe],
            columns=self.decision_names
        )
        """
        df_objs = pd.DataFrame(
            self.archive_objectives[nfe],
            columns=self.objective_names
        )

        # Create Plot
        cols = self.objective_names
        cols.reverse()
        color_col = self.objective_names[0]
        exp = hip.Experiment.from_dataframe(df_objs)
        exp.parameters_definition[color_col].colormap = 'interpolateViridis'
        exp.display_data(hip.Displays.PARALLEL_PLOT).update(
            {'order': cols}
        )
        exp.display_data(hip.Displays.TABLE).update(
            {'hide': ['uid', 'from_uid']}
        )

        return exp

class BorgRuntimeAggregator():
    """
    Agregate multiple runs of borg multi-objective algorithm runtime objects
    """
    def __init__(
        self,
        runtime_objs,
    ):
        """Initilization
        Parameters
        ----------
        runtime_objs : dict
            Dictionary with keys of run name and values being runtime
             objects
        """
        self.runs = runtime_objs

    def plot_hypervolume(self, reference_point):
        """
        Plot hypervolume over the search
        Parameters
        ----------
        reference_point : list
            Reference point for hypervolume calculation
        Returns
        -------
        matplotlib.figure.Figure
            Plot of improvments
        """
        # Setup
        df_ls = []

        # Computing hypervolume
        for run_name, run_obj in self.runs.items():
            df_run = pd.DataFrame()
            run_obj.compute_hypervolume(reference_point)
            df_run['hypervolume'] = pd.Series(run_obj.hypervolume)
            df_run['run_name'] = run_name
            df_run['nfe'] = df_run.index
            df_ls.append(df_run)
        df = pd.concat(df_ls)

        # Plotting
        fig, ax = plt.subplots()
        sns.lineplot(data=df, x='nfe', y='hypervolume', hue='run_name', ax=ax)
        plt.ylabel('Hypervolume')
        plt.xlabel('Function Evaluations')
        ax.legend(title='Run')

        return fig

    def plot_interactive_front(self):
        """
        Plot interactive front at final search
        Returns
        -------
        matplotlib.figure.Figure
            Plot of improvments
        """
        # Setup
        df_ls = []

        for run_name, run_obj in self.runs.items():
            # Extract total function evaluations
            nfe = run_obj.nfe[-1]

            # Get front
            df_decs = pd.DataFrame(
                run_obj.archive_decisions[nfe],
                columns=run_obj.decision_names
            )
            df_objs = pd.DataFrame(
                run_obj.archive_objectives[nfe],
                columns=run_obj.objective_names
            )
            df_metrics = pd.DataFrame(
                run_obj.archive_metrics[nfe],
                columns=run_obj.metric_names
            )
            df_front = pd.concat([df_decs, df_objs, df_metrics], axis=1)
            df_front['run_name'] = run_name

            # Store
            df_ls.append(df_front)

        # Making parent dataframe
        df = pd.concat(df_ls)

        # Create Plot
        cols = \
            run_obj.decision_names +\
            run_obj.objective_names +\
            run_obj.metric_names +\
            ['run_name']
        cols.reverse()
        color_col = 'run_name'
        exp = hip.Experiment.from_dataframe(df)
        exp.parameters_definition[color_col].colormap = 'schemeDark2'
        exp.display_data(hip.Displays.PARALLEL_PLOT).update(
            {'order': cols, 'hide': ['uid']},
        )
        exp.display_data(hip.Displays.TABLE).update(
            {'hide': ['uid', 'from_uid']}
        )

        return exp
