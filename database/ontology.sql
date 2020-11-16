
-- <https://cso.kmi.open.ac.uk/topics/random_projections>,<http://cso.kmi.open.ac.uk/schema/cso#relatedEquivalent>,<https://cso.kmi.open.ac.uk/topics/random_projection>
-- drop table medical_informatics.cso_unique_concept;
create materialized view if not exists medical_informatics.cso_unique_concept ENGINE = Log populate as
select arrayJoin(
               arrayDistinct(
                       arrayFilter(x->position(x, '/') == 0,
                                   arrayFlatten(groupArray([sbj, obj]))))) as cso_original_ontology,
       replaceAll(lower(cso_original_ontology), '_', ' ')                  as concept
from (
      select replaceAll(replaceAll(
                                replaceAll(
                                        replaceAll(replaceAll(replaceAll(subject, 'http://', ''), 'https://', ''), '<',
                                                   ''), '>', ''),
                                'cso.kmi.open.ac.uk/', ''), 'topics/', '') as sbj,
             position(replaceAll(replaceAll(replaceAll(replaceAll(replaceAll(relation, 'http://', ''), 'https://', ''),
                                                       '<', ''), '>',
                                            ''), 'cso.kmi.open.ac.uk/', '') as temp_pred, 'schema/cso#') ==
             0 ?
             replaceAll(substring(temp_pred, position(temp_pred, '#') + 1), 'schema.org/', '')
                 : replaceAll(temp_pred, 'schema/cso#', '')                as pred,
             replaceAll(replaceAll(
                                replaceAll(
                                        replaceAll(replaceAll(replaceAll(object, 'http://', ''), 'https://', ''), '<',
                                                   ''), '>',
                                        ''),
                                'cso.kmi.open.ac.uk/', ''), 'topics/', '') as obj
      from medical_informatics.cso);
-- 26475
select count()
from medical_informatics.cso_unique_concept;

with (select groupArray([cso_original_ontology, concept]) as cso_concept_list
      from medical_informatics.cso_unique_concept) as cso_concept_list
select keyword_id,
       document_unique_id,
       keyword,
       arrayMap(x ->
                    (x, (length(arrayIntersect(splitByChar(' ', lower(keyword)) as a1,
                                               splitByChar(' ', lower(x[2])) as a2)) as len_intersect) * 1.0 /
                        (length(a1) + length(a2) - len_intersect))
           , cso_concept_list) as matched_most_sim_cso_list

from medical_informatics.wos_keyword;

with [1,2,3,4] as a1, [3,4,5,6,7,8,9] as a2
select (length(arrayIntersect(a1, a2)) as len_intersect) * 1.0 /
       (length(a1) + length(a2) - len_intersect) as jaccard_sim;