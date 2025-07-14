from flamapy.core.discover import DiscoverMetamodels
from flamapy.metamodels.configuration_metamodel.models import Configuration
from flamapy.metamodels.bdd_metamodel.operations import (
    BDDConfigurationsNumber,
    BDDProductDistribution,
    BDDFeatureInclusionProbability,
    BDDSampling
)
from flamapy.metamodels.bdd_metamodel.transformations import FmToBDD


FM_MODEL = 'resources/models/uvl_models/Pizzas.uvl'


def main() -> None:
    dm = DiscoverMetamodels()
    fm_model = dm.use_transformation_t2m(FM_MODEL, 'fm')
    bdd_model = FmToBDD(fm_model).transform()
    print(f'BDD model: {bdd_model}')
    print(bdd_model.mapping_names)

    n_configs = BDDConfigurationsNumber().execute(bdd_model).get_result()
    print(f'Number of configurations: {n_configs}')

    elements = ['Ice Cream', 'Vanilla']
    config = Configuration({f: True for f in elements})
    op_config = BDDConfigurationsNumber()
    op_config.set_partial_configuration(config)
    n_configs = op_config.execute(bdd_model).get_result()
    print(f'Number of configurations (from partial config): {n_configs}')

    pdist = BDDProductDistribution().execute(bdd_model).get_result()
    print(f'Product distribution: {pdist} ({sum(pdist)})')

    fip = BDDFeatureInclusionProbability().execute(bdd_model).get_result()
    print(f'Feature inclusion probabilities: {fip}')

    op_fip = BDDFeatureInclusionProbability()
    op_fip.set_partial_configuration(config)
    fip = op_fip.execute(bdd_model).get_result()
    print(f'Feature inclusion probabilities (from partial config): {fip}')

    op_sampling = BDDSampling()
    op_sampling.set_sample_size(5)
    sample = op_sampling.execute(bdd_model).get_result()
    for i, config in enumerate(sample):
        print(f'P {i}: {config}')

    # configs = BDDConfigurations().execute(bdd_model).get_result()
    # for i, config in enumerate(configs):
    #     print(f'P {i}: {config}')
    # print(f'Products: {len(configs)}')


if __name__ == "__main__":
    main()
