<script>
import CrudList from './CrudList';

export default {
  name: 'CrudTokenList',
  extends: CrudList,
  data: () => ({
    createable: true,
    updateable: false,
    destroyable: true,
    headlines: {
      table: 'Tokens',
      create: 'Generate New Token',
      destroy: 'Token Deletion',
    },
    texts: {
      create: () => ('Names are purely for your own convenience and carry no technical meaning.'),
      destroy: d => (`Delete token with name "${d.name}" (${d.id})?`),
      destroyWarning: () => 'This operation is permanent. Any devices using this token will no longer be able to authenticate.',
    },
    columns: {
      id: {
        text: 'ID',
        align: 'left',
        value: 'id',
        readonly: true,
        datatype: 'GenericText',
        searchable: true,
      },
      name: {
        text: 'Name',
        textCreate: 'Enter token name',
        align: 'left',
        sortable: true,
        value: 'name',
        readonly: false,
        writeOnCreate: true,
        datatype: 'GenericText',
        searchable: true,
      },
      created: {
        text: 'Created',
        align: 'left',
        sortable: true,
        value: 'created',
        readonly: true,
        datatype: 'TimeAgo',
        searchable: false,
      },
    },
    actions: [],
    paths: {
      list: 'auth/tokens/',
      create: 'auth/tokens/',
      delete: 'auth/tokens/:{id}/',
    },
    defaultObject: { name: '' },
    postcreate: d => (alert(`postcreate ${d.name}`)),
    // TODO rowclick(domain) { this.$router.push({ name: 'CrudDomain', params: { name: domain.name } }); },
  }),
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
