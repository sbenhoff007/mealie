<template>
  <v-container v-if="group" class="narrow-container">
    <BasePageTitle>
      <template #header>
        <v-img max-height="125" max-width="125" :src="require('~/static/svgs/manage-group-settings.svg')"></v-img>
      </template>
      <template #title> {{ $t('group.admin-group-management') }} </template>
      {{ $t('group.admin-group-management-text') }}
    </BasePageTitle>
    <AppToolbar back> </AppToolbar>
    <v-card-text> {{ $t('group.group-id-value', [group.id]) }} </v-card-text>
    <v-form v-if="!userError" ref="refGroupEditForm" @submit.prevent="handleSubmit">
      <v-card outlined>
        <v-card-text>
          <v-text-field v-model="group.name" :label="$t('group.group-name')"> </v-text-field>
          <GroupPreferencesEditor v-if="group.preferences" v-model="group.preferences" />
        </v-card-text>
      </v-card>
      <div class="d-flex pa-2">
        <BaseButton type="submit" edit class="ml-auto"> {{ $t("general.update") }}</BaseButton>
      </div>
    </v-form>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, useRoute, onMounted, ref, useContext } from "@nuxtjs/composition-api";
import GroupPreferencesEditor from "~/components/Domain/Group/GroupPreferencesEditor.vue";
import { useAdminApi } from "~/composables/api";
import { alert } from "~/composables/use-toast";
import { GroupInDB } from "~/lib/api/types/user";
import { VForm } from "~/types/vuetify";

export default defineComponent({
  components: {
    GroupPreferencesEditor,
  },
  layout: "admin",
  setup() {
    const route = useRoute();

    const { i18n } = useContext();

    const groupId = route.value.params.id;

    // ==============================================
    // New User Form

    const refGroupEditForm = ref<VForm | null>(null);

    const adminApi = useAdminApi();

    const group = ref<GroupInDB | null>(null);

    const userError = ref(false);

    onMounted(async () => {
      const { data, error } = await adminApi.groups.getOne(groupId);

      if (error?.response?.status === 404) {
        alert.error(i18n.tc("user.user-not-found"));
        userError.value = true;
      }

      if (data) {
        group.value = data;
      }
    });

    async function handleSubmit() {
      if (!refGroupEditForm.value?.validate() || group.value === null) {
        return;
      }

      const { response, data } = await adminApi.groups.updateOne(group.value.id, group.value);
      if (response?.status === 200 && data) {
        group.value = data;
      }
    }

    return {
      group,
      userError,
      refGroupEditForm,
      handleSubmit,
    };
  },
});
</script>
