<script>
import { ipAddress } from 'vuelidate/lib/validators';
import Record from './Record.vue';

export default {
  name: 'RecordA',
  extends: Record,
  data: () => ({
    errors: {
      ipAddress: 'This field must contain an IPv4 address.',
    },
    fields: [
      { validations: { ipAddress } },
    ],
  }),
};
</script>
