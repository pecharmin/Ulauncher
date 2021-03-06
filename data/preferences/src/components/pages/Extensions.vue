<template>
  <div class="page row">

    <div class="left-nav col-4">

      <ul class="ext-list">
        <li
          v-for="(ext, idx) in extensions"
          :class="{active: ext.id == activeExt.id, last: idx == extensions.length - 1}"
          @click="selectExtension(ext)"
          >
          <i class="ext-icon" :style="{'background-image': `url('${ext.icon}')`}"></i>
          <span>{{ ext.name }}</span>
        </li>
        <li class="link" @click="addExtDialog"><i class="fa fa-plus"></i> <span>Add extension</span></li>
        <li class="link" @click="openUrlInBrowser('https://ext.ulauncher.io')"><i class="fa fa-external-link"></i> <span>Discover extensions</span></li>
        <li class="link" @click="openUrlInBrowser('http://docs.ulauncher.io')"><i class="fa fa-external-link"></i> <span>Create your own</span></li>
      </ul>

      <b-modal
        ref="addExtForm"
        ok-title="Add"
        close-title="Cancel"
        hide-header-close
        no-auto-focus
        @shown="onAddExtFormShown"
        @ok="onModalOk">
          <template slot="modal-title">
            Enter extension URL
          </template>

          <b-form @submit.native.prevent="onUrlSubmit">
            <b-form-input
              class="github-url-input"
              ref="githubUrl"
              type="text"
              placeholder="https://github.com/org-name/project-name"></b-form-input>
          </b-form>

          <div v-if="addingExtension" class="adding-ext-msg">
            <i class="fa fa-spinner fa-spin"></i> Downloading extension...
          </div>

          <div v-if="addingExtensionError" class="adding-ext-msg warning selectable">
            <i class="fa fa-warning"></i> {{ addingExtensionError }}
          </div>
      </b-modal>

    </div>

    <div class="col-8 ext-view">
        <extension-config
          v-if="activeExt"
          @removed="onRemoved"
          :extension="activeExt"></extension-config>
    </div>
  </div>
</template>

<script>
import jsonp from '@/api'
import bus from '@/event-bus'
import ExtensionConfig from '@/components/pages/ExtensionConfig'

export default {
  name: 'extensions',
  created () {
    this.fetchData()
  },
  components: {
    'extension-config': ExtensionConfig
  },
  data () {
    return {
      activeExt: null,
      addingExtension: false,
      addingExtensionError: '',
      extensions: []
    }
  },
  methods: {
    fetchData () {
      jsonp('prefs://extension/get-all').then((data) => {
        this.extensions = data
        this.activeExt = data[0]
      }, (err) => bus.$emit('error', err))
    },
    onAddExtFormShown () {
      this.$nextTick(() => this.$refs.githubUrl.focus())
      this.addingExtensionError = ''
    },
    addExtDialog () {
      this.$refs.addExtForm.show()
    },
    openUrlInBrowser (url) {
      jsonp('prefs://open/web-url', {url: url})
    },
    selectExtension (ext) {
      this.activeExt = ext
    },
    onRemoved (id) {
      for (let i = 0; i < this.extensions.length; i++) {
        if (this.extensions[i].id === id) {
          this.$delete(this.extensions, i)
          this.activeExt = this.extensions.length ? this.extensions[0] : null
          break
        }
      }
    },
    setActiveByUrl (url) {
      for (let i = 0; i < this.extensions.length; i++) {
        if (this.extensions[i].url === url) {
          this.activeExt = this.extensions[i]
          break
        }
      }
    },
    onModalOk (e) {
      let input = this.$refs.githubUrl.$el
      if (!input.value) {
        return e.cancel()
      }

      this.addExtension(input)

      return e.cancel()
    },
    onUrlSubmit () {
      let input = this.$refs.githubUrl.$el
      if (input.value) {
        this.addExtension(input)
      }
    },
    addExtension (input) {
      this.addingExtension = true
      this.addingExtensionError = ''
      jsonp('prefs://extension/add', {url: input.value}).then((data) => {
        this.extensions = data
        this.addingExtension = false
        this.setActiveByUrl(input.value)
        input.value = ''
        this.$refs.addExtForm.hide()
      }, (err) => {
        this.addingExtension = false
        this.addingExtensionError = err
      })
    }
  }
}
</script>

<style lang="scss" scoped>
$darkBlue: #015aa7;
$veryLightGrey: #c8c8c8;

.page {
  padding: 20px 15px 15px 25px;
}
.adding-ext-msg {
  overflow: auto;
  color: #555;
  padding-top: 10px;
}
.warning {color: #b30000}
.ext-list {
  $listIconSize: 17px;

  list-style: none;
  padding: 0;
  margin: 0;
  margin-bottom: 10px;

  li {
    cursor: pointer;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
    text-align: left;
    position: relative;
    padding: 3px 0;
    margin: 3px 0;
    color: #555;

    i {
      margin-right: 5px;
      width: $listIconSize;
      height: $listIconSize;
    }

    .ext-icon {
      display: inline-block;
      background-repeat: no-repeat;
      background-size: $listIconSize $listIconSize;
      position: relative;
      top: 3px;
    }

    &.active,
    &:hover {
      color: $darkBlue;
    }

    &.active span,
    &:hover span {
      text-decoration: underline;
    }

    &.last {
      margin-bottom: 25px;
    }
  }

  .link {
    font-style: italic;
  }

}
</style>
